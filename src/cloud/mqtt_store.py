import json
import logging
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import paho.mqtt.client as mqtt

LOG = logging.getLogger("iiot-dashboard")
DATABASE = Path(os.getenv("DATABASE_PATH", "/data/iiot.sqlite3"))
MQTT_HOST = os.getenv("MQTT_HOST", "158.180.44.197")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "bobm")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TLS = os.getenv("MQTT_TLS", "false").lower() in {"1", "true", "yes"}

DB_LOCK = threading.Lock()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def connect_db() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with DB_LOCK, connect_db() as db:
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


def parse_topic(topic: str) -> tuple[str | None, str | None]:
    parts = topic.split("/")
    if len(parts) == 4 and parts[:2] == ["iiot", "group"] and parts[3] == "status":
        return parts[2], "status"
    if (
        len(parts) == 6
        and parts[:2] == ["iiot", "group"]
        and parts[3] == "sensor"
        and parts[5] == "state"
    ):
        return parts[2], parts[4]
    return None, None


def _iso_timestamp(value: Any, fallback: str) -> str:
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        except ValueError:
            pass
    # Several course devices publish millis() rather than Unix time. Such values
    # are not wall-clock timestamps, so reception time is the honest fallback.
    return fallback


def normalize_readings(
    topic_sensor: str, payload: dict[str, Any], received_at: str
) -> list[dict[str, Any]]:
    timestamp = _iso_timestamp(payload.get("timestamp"), received_at)
    sensor_id = payload.get("sensor_id") or payload.get("sensorId") or payload.get("source")
    status = str(payload.get("status", "ok"))

    if "value" in payload:
        return [{
            "sensor_type": topic_sensor,
            "sensor_id": sensor_id,
            "measured_at": timestamp,
            "value": float(payload["value"]),
            "unit": str(payload.get("unit", "")),
            "status": status,
        }]

    # Be tolerant of combined payloads observed on the course broker.
    units = {"temperature": "°C", "humidity": "%"}
    readings = []
    for name, unit in units.items():
        value = payload.get(name)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            readings.append({
                "sensor_type": name,
                "sensor_id": sensor_id,
                "measured_at": timestamp,
                "value": float(value),
                "unit": unit,
                "status": status,
            })
    return readings


def store_message(topic: str, raw_payload: bytes) -> int:
    group, message_type = parse_topic(topic)
    if not group:
        return 0
    received_at = utc_now()
    try:
        decoded = json.loads(raw_payload.decode("utf-8"))
        with DB_LOCK, connect_db() as db:
            if message_type == "status":
                payload = decoded if isinstance(decoded, dict) else {"status": decoded}
                status = str(payload.get("status", "unknown"))
                db.execute(
                    """INSERT INTO device_status
                       (group_name, sensor_id, status, measured_at, received_at, topic)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ON CONFLICT(group_name) DO UPDATE SET
                         sensor_id=excluded.sensor_id, status=excluded.status,
                         measured_at=excluded.measured_at, received_at=excluded.received_at,
                         topic=excluded.topic""",
                    (group, payload.get("sensor_id") or payload.get("sensorId"), status,
                     payload.get("timestamp"), received_at, topic),
                )
                return 1
            if not isinstance(decoded, dict):
                return 0
            rows = normalize_readings(message_type, decoded, received_at)
            db.executemany(
                """INSERT INTO readings
                   (group_name, sensor_type, sensor_id, measured_at, received_at,
                    value, unit, status, topic)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [(group, row["sensor_type"], row["sensor_id"], row["measured_at"],
                  received_at, row["value"], row["unit"], row["status"], topic)
                 for row in rows],
            )
            return len(rows)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as error:
        LOG.warning("Rejected message on %s: %s", topic, error)
        return 0


class MqttCollector:
    def __init__(self) -> None:
        initialize_database()
        self.connected = False
        self.last_error = ""
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"iiot-streamlit-{uuid4().hex[:10]}",
            protocol=mqtt.MQTTv5,
        )
        if MQTT_USER:
            self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        if MQTT_TLS:
            self.client.tls_set()
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.connect_async(MQTT_HOST, MQTT_PORT, keepalive=60)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, reason_code, properties) -> None:
        self.connected = reason_code == 0
        self.last_error = "" if self.connected else str(reason_code)
        if self.connected:
            client.subscribe("iiot/group/#", qos=1)

    def _on_disconnect(self, client, userdata, flags, reason_code, properties) -> None:
        self.connected = False
        if reason_code != 0:
            self.last_error = str(reason_code)

    @staticmethod
    def _on_message(client, userdata, message) -> None:
        store_message(message.topic, message.payload)

