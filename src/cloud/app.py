import json
import logging
import os
import sqlite3
import threading
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request
import paho.mqtt.client as mqtt

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
LOG = logging.getLogger("iiot-dashboard")

DATABASE = Path(os.getenv("DATABASE_PATH", "/data/iiot.sqlite3"))
MQTT_HOST = os.getenv("MQTT_HOST", "158.180.44.197")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "bobm")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TLS = os.getenv("MQTT_TLS", "false").lower() in {"1", "true", "yes"}

app = Flask(__name__)
db_lock = threading.Lock()


def connect_db():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with db_lock, closing(connect_db()) as db:
        db.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL,
                sensor_type TEXT NOT NULL,
                sensor_id TEXT,
                measured_at TEXT NOT NULL,
                received_at TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                status TEXT NOT NULL,
                topic TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_readings_lookup
                ON readings(group_name, sensor_type, measured_at);
            CREATE TABLE IF NOT EXISTS device_status (
                group_name TEXT PRIMARY KEY,
                sensor_id TEXT,
                status TEXT NOT NULL,
                measured_at TEXT,
                received_at TEXT NOT NULL,
                topic TEXT NOT NULL
            );
            """
        )
        db.commit()


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_topic(topic):
    parts = topic.split("/")
    if len(parts) == 4 and parts[:2] == ["iiot", "group"] and parts[3] == "status":
        return parts[2], "status"
    if len(parts) == 6 and parts[:2] == ["iiot", "group"] and parts[3] == "sensor" and parts[5] == "state":
        return parts[2], parts[4]
    return None, None


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code != 0:
        LOG.error("MQTT connection failed: %s", reason_code)
        return
    LOG.info("Connected to MQTT broker %s:%s", MQTT_HOST, MQTT_PORT)
    client.subscribe("iiot/group/+/sensor/+/state", qos=1)
    client.subscribe("iiot/group/+/status", qos=1)


def on_message(client, userdata, message):
    group_name, message_type = parse_topic(message.topic)
    if not group_name:
        return
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        received_at = utc_now()
        with db_lock, closing(connect_db()) as db:
            if message_type == "status":
                status = str(payload["status"])
                if status not in {"ok", "error", "offline"}:
                    raise ValueError("invalid status")
                db.execute(
                    """INSERT INTO device_status
                       (group_name, sensor_id, status, measured_at, received_at, topic)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ON CONFLICT(group_name) DO UPDATE SET
                         sensor_id=excluded.sensor_id, status=excluded.status,
                         measured_at=excluded.measured_at, received_at=excluded.received_at,
                         topic=excluded.topic""",
                    (group_name, payload.get("sensor_id"), status,
                     payload.get("timestamp"), received_at, message.topic),
                )
            else:
                value = float(payload["value"])
                measured_at = str(payload["timestamp"])
                unit = str(payload["unit"])
                status = str(payload.get("status", "ok"))
                db.execute(
                    """INSERT INTO readings
                       (group_name, sensor_type, sensor_id, measured_at, received_at,
                        value, unit, status, topic)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (group_name, message_type, payload.get("sensor_id"), measured_at,
                     received_at, value, unit, status, message.topic),
                )
            db.commit()
    except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as error:
        LOG.warning("Rejected message on %s: %s", message.topic, error)


def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="iiot-group1-dashboard")
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    if MQTT_TLS:
        client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()
    return client


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/sensors")
def sensors():
    with closing(connect_db()) as db:
        rows = db.execute(
            """SELECT r.group_name, r.sensor_type, r.sensor_id,
                      COUNT(*) AS samples, MIN(r.value) AS minimum,
                      MAX(r.value) AS maximum, AVG(r.value) AS average,
                      MAX(r.measured_at) AS last_measurement,
                      s.status AS device_status, s.received_at AS last_status_received
               FROM readings r
               LEFT JOIN device_status s ON s.group_name = r.group_name
               GROUP BY r.group_name, r.sensor_type, r.sensor_id
               ORDER BY r.group_name, r.sensor_type"""
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.get("/api/readings")
def readings():
    group_name = request.args.get("group")
    sensor_type = request.args.get("sensor", "temperature")
    limit = min(max(request.args.get("limit", 200, type=int), 1), 2000)
    query = "SELECT * FROM readings WHERE sensor_type = ?"
    parameters = [sensor_type]
    if group_name:
        query += " AND group_name = ?"
        parameters.append(group_name)
    query += " ORDER BY measured_at DESC LIMIT ?"
    parameters.append(limit)
    with closing(connect_db()) as db:
        rows = db.execute(query, parameters).fetchall()
    return jsonify([dict(row) for row in reversed(rows)])


DASHBOARD = """
<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IIoT Sensor Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
body{font-family:system-ui;margin:0;background:#0f172a;color:#e2e8f0}main{max-width:1200px;margin:auto;padding:24px}
h1{margin-bottom:4px}.muted{color:#94a3b8}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:22px 0}
.card,.chart{background:#1e293b;border-radius:12px;padding:16px}.ok{color:#4ade80}.error,.offline{color:#fb7185}
select{background:#334155;color:white;padding:8px;border:0;border-radius:6px}canvas{max-height:430px}
</style></head><body><main><h1>IIoT Sensor Dashboard</h1><p class="muted">Live-Daten aller Gruppen · automatische Aktualisierung</p>
<label>Gruppe: <select id="group"></select></label><section class="cards" id="cards"></section>
<section class="chart"><canvas id="chart"></canvas></section></main>
<script>
let chart; async function refresh(){const sensors=await fetch('/api/sensors').then(r=>r.json());
const groups=[...new Set(sensors.map(s=>s.group_name))];const select=document.querySelector('#group');
const previous=select.value;if(select.options.length!==groups.length){select.innerHTML=groups.map(g=>`<option>${g}</option>`).join('');if(groups.includes(previous))select.value=previous;}
const group=select.value||groups[0];const rows=sensors.filter(s=>s.group_name===group);
document.querySelector('#cards').innerHTML=rows.map(s=>`<article class="card"><strong>${s.sensor_type}</strong><p>Status: <span class="${s.device_status}">${s.device_status||'unbekannt'}</span></p><p>${s.samples} Werte</p><small>Min ${fmt(s.minimum)} · Ø ${fmt(s.average)} · Max ${fmt(s.maximum)}</small></article>`).join('');
if(!group)return;const data=await fetch(`/api/readings?group=${encodeURIComponent(group)}&sensor=temperature`).then(r=>r.json());
const config={type:'line',data:{labels:data.map(x=>x.measured_at),datasets:[{label:'Temperatur °C',data:data.map(x=>x.value),borderColor:'#38bdf8',tension:.2}]},options:{responsive:true,scales:{x:{ticks:{color:'#94a3b8'}},y:{ticks:{color:'#94a3b8'}}}}};
if(chart)chart.destroy();chart=new Chart(document.querySelector('#chart'),config)}function fmt(v){return v==null?'–':Number(v).toFixed(2)}
document.querySelector('#group').addEventListener('change',refresh);refresh();setInterval(refresh,10000);
</script></body></html>
"""


@app.get("/")
def dashboard():
    return render_template_string(DASHBOARD)


initialize_database()
mqtt_client = None if os.getenv("DISABLE_MQTT") == "1" else start_mqtt()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

