"""Prueft das Grafana-Dashboard: Struktur und alle SQL-Abfragen gegen eine Test-Datenbank.

Die Variablen werden so ersetzt, wie Grafana es tut ($group, ${sensor:sqlstring},
$unit, $__from/$__to in Millisekunden). Grafana selbst wird dafuer nicht benoetigt.
"""
import importlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
DASHBOARD = json.loads((REPO / "grafana/dashboards/iiot.json").read_text(encoding="utf-8"))
DATASOURCE = yaml.safe_load((REPO / "grafana/provisioning/datasources/sqlite.yml").read_text(encoding="utf-8"))
GROUP = "unterhuber-brachmann-reimeir-noessing"


def all_panels():
    for panel in DASHBOARD["panels"]:
        yield panel
        yield from panel.get("panels", [])


def interpolate(sql, group=GROUP, sensors=("temperature", "humidity", "hygrometer-1", "hygrometer-2"),
                unit="%", hours=24):
    now = datetime.now(timezone.utc)
    sql = sql.replace("${sensor:sqlstring}", ",".join(f"'{s}'" for s in sensors))
    sql = sql.replace("$group", group).replace("$unit", unit)
    sql = sql.replace("$__from", str(int((now - timedelta(hours=hours)).timestamp() * 1000)))
    sql = sql.replace("$__to", str(int(now.timestamp() * 1000)))
    assert "$" not in sql, f"nicht ersetzte Variable in: {sql}"
    return sql


@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "t.sqlite3"))
    monkeypatch.syspath_prepend(str(REPO / "src/cloud"))
    sys.modules.pop("mqtt_store", None)
    store = importlib.import_module("mqtt_store")
    store.initialize_database()
    now = datetime.now(timezone.utc)
    for i in range(120):
        ts = (now - timedelta(minutes=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        for sensor, value, unit in [("temperature", 21 + i / 100, "°C"), ("humidity", 40.0, "%"),
                                    ("hygrometer-1", 30.0, "%"), ("hygrometer-2", 55.5, "%")]:
            store.store_message(f"iiot/group/{GROUP}/sensor/{sensor}/state",
                                json.dumps({"timestamp": ts, "sensor_id": "a", "value": value, "unit": unit}).encode())
        # zweites Geraet derselben Gruppe in derselben Sekunde
        store.store_message(f"iiot/group/{GROUP}/sensor/temperature/state",
                            json.dumps({"timestamp": ts, "sensor_id": "b", "value": 25.0, "unit": "°C"}).encode())
    store.store_message(f"iiot/group/{GROUP}/status", b'{"status":"ok"}')
    store.store_message("iiot/group/andere-gruppe/sensor/dht/state", b'{"temperature": 5, "humidity": 50}')
    # Millisekunden-Zeitstempel im Format 2026-...T...123456Z (received_at)
    return store.connect_db()


def test_structure():
    uid = DATASOURCE["datasources"][0]["uid"]
    assert DATASOURCE["datasources"][0]["type"] == "frser-sqlite-datasource"
    ids = [p["id"] for p in all_panels()]
    assert len(ids) == len(set(ids))
    variables = {v["name"] for v in DASHBOARD["templating"]["list"]}
    for panel in all_panels():
        if panel["type"] == "row":
            continue
        assert panel["datasource"]["uid"] == uid
        for target in panel["targets"]:
            assert target["datasource"]["uid"] == uid
            assert target["rawQueryText"] == target["queryText"]
            assert target["queryType"] in {"table", "time series"}
            for name in re.findall(r"\$\{?(\w+)", target["rawQueryText"]):
                assert name.startswith("__") or name in variables, name
        if "repeat" in panel:
            assert panel["repeat"] in variables


def test_no_en_dash_anywhere():
    for path in [*(REPO / "grafana").rglob("*"), REPO / "docker-compose.yml"]:
        if path.is_file():
            assert "–" not in path.read_text(encoding="utf-8"), path


def test_variable_queries(db):
    results = {}
    for var in DASHBOARD["templating"]["list"]:
        cursor = db.execute(interpolate(var["query"]))
        assert len(cursor.description) == 1, var["name"]
        results[var["name"]] = [r[0] for r in cursor.fetchall()]
    assert GROUP in results["group"] and "andere-gruppe" in results["group"]
    assert results["sensor"] == ["humidity", "hygrometer-1", "hygrometer-2", "temperature"]
    assert results["unit"] == ["%", "°C"]


@pytest.mark.parametrize("panel", [p for p in all_panels() if p["type"] != "row"], ids=lambda p: p["title"])
def test_panel_queries(db, panel):
    for target in panel["targets"]:
        for unit in ("%", "°C"):
            cursor = db.execute(interpolate(target["rawQueryText"], unit=unit))
            columns = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            assert rows, f"{panel['title']}: keine Daten"
            for col in target["timeColumns"]:
                if col in columns:
                    idx = columns.index(col)
                    assert all(isinstance(r[idx], int) and r[idx] > 1.7e9 for r in rows), "time muss Unix-Sekunden sein"
            if target["queryType"] == "time series":
                # Voraussetzung fuer die Long-to-Wide-Umwandlung im Plugin
                assert columns == ["time", "sensor_type", "value"]
                times = [r[0] for r in rows]
                assert times == sorted(times)
                assert len({(r[0], r[1]) for r in rows}) == len(rows)
                units = {r[1] for r in rows}
                if "$unit" in target["rawQueryText"]:
                    assert units == (
                        {"temperature"} if unit == "°C" else {"humidity", "hygrometer-1", "hygrometer-2"})
                else:
                    assert units == {"temperature", "humidity", "hygrometer-1", "hygrometer-2"}


def test_time_window_filters(db):
    panel = next(p for p in all_panels() if p["title"] == "Werte im Zeitraum")
    sql = panel["targets"][0]["rawQueryText"]
    one_hour = db.execute(interpolate(sql, hours=1)).fetchone()[0]
    day = db.execute(interpolate(sql, hours=24)).fetchone()[0]
    assert 0 < one_hour < day


def test_last_message_is_recent(db):
    panel = next(p for p in all_panels() if p["title"] == "Letzte Nachricht")
    value = db.execute(interpolate(panel["targets"][0]["rawQueryText"])).fetchone()[0]
    assert abs(value / 1000 - datetime.now(timezone.utc).timestamp()) < 60


def test_status(db):
    panel = next(p for p in all_panels() if p["title"] == "Gerätestatus")
    assert [tuple(r) for r in db.execute(interpolate(panel["targets"][0]["rawQueryText"]))] == [("ok",)]
