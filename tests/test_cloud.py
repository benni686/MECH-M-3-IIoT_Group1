import importlib.util
import json
import os
from pathlib import Path


def load_cloud(tmp_path):
    os.environ["DATABASE_PATH"] = str(tmp_path / "test.sqlite3")
    os.environ["MQTT_HOST"] = "localhost"
    os.environ["DISABLE_MQTT"] = "1"
    spec = importlib.util.spec_from_file_location("cloud_app", Path(__file__).parents[1] / "src/cloud/app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Message:
    topic = "iiot/group/unterhuber-brachmann-reimeir-noessing/sensor/temperature/state"
    payload = json.dumps({"timestamp": "2026-11-02T10:00:00Z", "sensor_id": "yourmuesli-innsbruck-01", "value": 22.5, "unit": "°C", "status": "ok"}).encode()


def test_mqtt_reading_is_stored_and_exposed(tmp_path):
    cloud = load_cloud(tmp_path)
    cloud.on_message(None, None, Message())
    client = cloud.app.test_client()
    readings = client.get("/api/readings?group=unterhuber-brachmann-reimeir-noessing").get_json()
    assert readings[0]["value"] == 22.5
    assert client.get("/health").get_json() == {"status": "ok"}


def test_topic_parser_accepts_sensor_and_status_topics(tmp_path):
    cloud = load_cloud(tmp_path)
    assert cloud.parse_topic("iiot/group/team/sensor/temperature/state") == ("team", "temperature")
    assert cloud.parse_topic("iiot/group/team/status") == ("team", "status")
    assert cloud.parse_topic("invalid/topic") == (None, None)
