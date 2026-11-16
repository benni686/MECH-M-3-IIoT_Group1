import os
from datetime import datetime, timedelta, timezone

import pandas as pd
import streamlit as st

from mqtt_store import MqttCollector, connect_db, initialize_database

st.set_page_config(page_title="IIoT Live-Daten", page_icon="📈", layout="wide")


@st.cache_resource
def start_collector() -> MqttCollector | None:
    initialize_database()
    if os.getenv("DISABLE_MQTT") == "1":
        return None
    return MqttCollector()


def load_catalog() -> pd.DataFrame:
    with connect_db() as db:
        return pd.read_sql_query(
            """SELECT r.group_name, r.sensor_type, r.unit, COUNT(*) AS samples,
                      MIN(r.measured_at) AS first_measurement,
                      MAX(r.measured_at) AS last_measurement,
                      s.status AS device_status
               FROM readings r
               LEFT JOIN device_status s ON s.group_name = r.group_name
               GROUP BY r.group_name, r.sensor_type, r.unit, s.status
               ORDER BY r.group_name, r.sensor_type""",
            db,
        )


def load_readings(group: str, sensors: list[str], since: datetime, limit: int) -> pd.DataFrame:
    placeholders = ",".join("?" for _ in sensors)
    query = f"""SELECT measured_at, received_at, sensor_type, sensor_id, value, unit, status
                FROM readings
                WHERE group_name = ? AND sensor_type IN ({placeholders})
                  AND measured_at >= ?
                ORDER BY measured_at DESC LIMIT ?"""
    parameters = [group, *sensors, since.isoformat().replace("+00:00", "Z"), limit]
    with connect_db() as db:
        frame = pd.read_sql_query(query, db, params=parameters)
    if not frame.empty:
        frame["measured_at"] = pd.to_datetime(frame["measured_at"], utc=True, errors="coerce")
        frame = frame.dropna(subset=["measured_at"]).sort_values("measured_at")
    return frame


collector = start_collector()

st.title("IIoT Sensor-Dashboard")
st.caption("Live-Daten vom Kurs-Broker · Topic `iiot/group/#` · automatische Aktualisierung alle 5 Sekunden")


@st.fragment(run_every="5s")
def dashboard() -> None:
    catalog = load_catalog()
    if catalog.empty:
        st.info("Noch keine Sensordaten empfangen. Verbindung und Zugangsdaten werden geprüft …")
        if collector and collector.last_error:
            st.error(f"MQTT-Verbindungsfehler: {collector.last_error}")
        return

    groups = catalog["group_name"].drop_duplicates().tolist()
    default_group = "unterhuber-brachmann-reimeir-noessing"
    default_index = groups.index(default_group) if default_group in groups else 0

    filter_a, filter_b, filter_c = st.columns([2, 3, 2])
    with filter_a:
        group = st.selectbox("Gruppe", groups, index=default_index)
    available = catalog.loc[catalog["group_name"] == group, "sensor_type"].drop_duplicates().tolist()
    with filter_b:
        sensors = st.multiselect("Sensoren", available, default=available)
    with filter_c:
        period = st.selectbox("Zeitraum", ["15 Minuten", "1 Stunde", "6 Stunden", "24 Stunden", "7 Tage"], index=3)

    if not sensors:
        st.warning("Bitte mindestens einen Sensor auswählen.")
        return

    durations = {
        "15 Minuten": timedelta(minutes=15), "1 Stunde": timedelta(hours=1),
        "6 Stunden": timedelta(hours=6), "24 Stunden": timedelta(days=1),
        "7 Tage": timedelta(days=7),
    }
    data = load_readings(group, sensors, datetime.now(timezone.utc) - durations[period], 20_000)
    if data.empty:
        st.info("Für diese Auswahl liegen im gewählten Zeitraum keine Werte vor.")
        return

    latest = data.sort_values("measured_at").groupby("sensor_type", as_index=False).tail(1)
    metric_columns = st.columns(min(len(latest), 4))
    for index, (_, row) in enumerate(latest.iterrows()):
        metric_columns[index % len(metric_columns)].metric(
            row["sensor_type"], f'{row["value"]:.2f} {row["unit"]}',
            help=f'Letzter Messwert: {row["measured_at"].tz_convert("Europe/Berlin").strftime("%d.%m.%Y %H:%M:%S %Z")}',
        )

    units = data["unit"].fillna("").unique().tolist()
    if len(units) > 1:
        st.caption("Die ausgewählten Sensoren verwenden verschiedene Einheiten; daher werden sie getrennt dargestellt.")
    for unit in units:
        subset = data[data["unit"].fillna("") == unit]
        chart_data = subset.pivot_table(
            index="measured_at", columns="sensor_type", values="value", aggfunc="last"
        )
        st.subheader(f"Zeitverlauf{' (' + unit + ')' if unit else ''}")
        st.line_chart(chart_data, x_label="Zeit", y_label=unit or "Messwert", height=400)

    with st.expander("Messdaten anzeigen"):
        shown = data.sort_values("measured_at", ascending=False).copy()
        shown["measured_at"] = shown["measured_at"].dt.tz_convert("Europe/Berlin")
        st.dataframe(shown, use_container_width=True, hide_index=True)

    status = catalog.loc[catalog["group_name"] == group, "device_status"].dropna()
    broker_state = "verbunden" if collector and collector.connected else "wird verbunden"
    device_state = status.iloc[0] if not status.empty else "unbekannt"
    st.caption(f"Broker: {broker_state} · Gerätestatus: {device_state} · {len(data):,} dargestellte Werte")


dashboard()

