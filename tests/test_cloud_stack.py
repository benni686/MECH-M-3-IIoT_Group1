"""Tests fuer den Cloud-Stack: mqtt_store.py, collector.py und streamlit_app.py."""
import importlib, json, os, sqlite3, subprocess, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pytest

REPO = Path(os.environ.get("REPO", Path(__file__).resolve().parents[1]))
CLOUD = REPO / "src/cloud"
GROUP = "unterhuber-brachmann-reimeir-noessing"


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "t.sqlite3"))
    monkeypatch.setenv("DISABLE_MQTT", "1")
    monkeypatch.syspath_prepend(str(CLOUD))
    sys.modules.pop("mqtt_store", None)
    mod = importlib.import_module("mqtt_store")
    mod.initialize_database()
    return mod


def rows(store, table="readings"):
    with store.connect_db() as db:
        return [dict(r) for r in db.execute(f"SELECT * FROM {table}")]


def topic(sensor):
    return f"iiot/group/{GROUP}/sensor/{sensor}/state"


def now_iso(delta=0):
    return (datetime.now(timezone.utc) - timedelta(minutes=delta)).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_spec_payload_from_our_esp32(store):
    p = {"timestamp": "2026-11-16T10:00:00Z", "sensor_id": "yourmuesli-innsbruck-01",
         "value": 22.5, "unit": "°C", "status": "ok"}
    assert store.store_message(topic("temperature"), json.dumps(p).encode()) == 1
    r = rows(store)[0]
    assert (r["group_name"], r["sensor_type"], r["value"], r["unit"]) == (GROUP, "temperature", 22.5, "°C")
    assert r["measured_at"] == "2026-11-16T10:00:00Z"


def test_all_four_esp32_topics(store):
    for s, u in [("temperature", "°C"), ("humidity", "%"), ("hygrometer-1", "%"), ("hygrometer-2", "%")]:
        store.store_message(topic(s), json.dumps({"timestamp": now_iso(), "value": 1.0, "unit": u}).encode())
    assert sorted(r["sensor_type"] for r in rows(store)) == ["humidity", "hygrometer-1", "hygrometer-2", "temperature"]


def test_combined_payload_without_timestamp(store):
    n = store.store_message(topic("dht"), json.dumps({"temperature": 21, "humidity": 40}).encode())
    assert n == 2
    assert {r["sensor_type"] for r in rows(store)} == {"temperature", "humidity"}


def test_millis_timestamp_falls_back_to_received(store):
    store.store_message(topic("temperature"), json.dumps({"timestamp": 123456, "value": 20, "unit": "°C"}).encode())
    r = rows(store)[0]
    assert r["measured_at"] == r["received_at"]


def test_timezone_offset_is_normalised_to_utc(store):
    store.store_message(topic("temperature"), json.dumps({"timestamp": "2026-11-16T11:00:00+01:00", "value": 20, "unit": "°C"}).encode())
    assert rows(store)[0]["measured_at"] == "2026-11-16T10:00:00Z"


def test_status_retained_and_lwt(store):
    store.store_message(f"iiot/group/{GROUP}/status", b'{"status":"ok","sensor_id":"x"}')
    store.store_message(f"iiot/group/{GROUP}/status", b'{"status":"offline"}')
    st = rows(store, "device_status")
    assert len(st) == 1 and st[0]["status"] == "offline"


@pytest.mark.parametrize("payload", [b"not json", b"\xff\xfe", b"[1,2]", b'{"value":"abc","unit":"C"}', b"42"])
def test_garbage_is_rejected_without_crash(store, payload):
    assert store.store_message(topic("temperature"), payload) == 0
    assert rows(store) == []


def test_invalid_topics_ignored(store):
    assert store.store_message("iiot/sensors/x/data", b'{"value":1}') == 0
    assert store.store_message("iiot/group/x/sensor/t", b'{"value":1}') == 0


def test_bool_value_in_combined_payload_ignored(store):
    assert store.store_message(topic("dht"), b'{"temperature": true}') == 0


def test_streamlit_app_renders_with_data(store, tmp_path):
    from streamlit.testing.v1 import AppTest
    for i in range(30):
        store.store_message(topic("temperature"), json.dumps({"timestamp": now_iso(i), "value": 20 + i / 10, "unit": "°C"}).encode())
        store.store_message(topic("humidity"), json.dumps({"timestamp": now_iso(i), "value": 40 + i / 10, "unit": "%"}).encode())
    store.store_message(topic("temperature").replace(GROUP, "other-group"), json.dumps({"timestamp": now_iso(), "value": 5, "unit": "°C"}).encode())
    store.store_message(f"iiot/group/{GROUP}/status", b'{"status":"ok"}')
    os.chdir(CLOUD)
    at = AppTest.from_file(str(CLOUD / "streamlit_app.py"), default_timeout=30).run()
    assert not at.exception, at.exception
    assert at.selectbox[0].value == GROUP
    assert set(at.multiselect[0].value) == {"humidity", "temperature"}
    assert len(at.metric) == 2
    # switch group and period
    at.selectbox[0].select("other-group").run()
    assert not at.exception, at.exception
    at.selectbox[1].select("15 Minuten").run()
    assert not at.exception, at.exception


def test_streamlit_app_renders_empty_db(store):
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(CLOUD / "streamlit_app.py"), default_timeout=30).run()
    assert not at.exception, at.exception
    assert any("Noch keine Sensordaten" in i.value for i in at.info)


def test_journal_mode_is_delete_for_grafana(store):
    with store.connect_db() as db:
        assert db.execute("PRAGMA journal_mode").fetchone()[0] == "delete"


def test_retained_redelivery_is_not_stored_twice(store):
    p = json.dumps({"timestamp": "2026-11-16T10:00:00Z", "value": 22.5, "unit": "°C"}).encode()
    assert store.store_message(topic("temperature"), p) == 1
    assert store.store_message(topic("temperature"), p, retained=True) == 0
    assert store.store_message(topic("temperature"), p, retained=True) == 0
    assert len(rows(store)) == 1


def test_retained_without_timestamp_is_skipped(store):
    assert store.store_message(topic("dht"), b'{"temperature": 21}', retained=True) == 0
    assert store.store_message(topic("dht"), b'{"temperature": 21}') == 1


def test_new_value_same_second_is_kept(store):
    for v in (1.0, 2.0):
        store.store_message(topic("temperature"), json.dumps({"timestamp": "2026-11-16T10:00:00Z", "value": v, "unit": "°C"}).encode())
    assert len(rows(store)) == 2


def test_old_wal_database_with_duplicates_is_migrated(tmp_path, monkeypatch):
    path = tmp_path / "old.sqlite3"
    db = sqlite3.connect(path)
    db.executescript("""PRAGMA journal_mode=WAL;
        CREATE TABLE readings (id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT NOT NULL,
          sensor_type TEXT NOT NULL, sensor_id TEXT, measured_at TEXT NOT NULL, received_at TEXT NOT NULL,
          value REAL NOT NULL, unit TEXT NOT NULL, status TEXT NOT NULL, topic TEXT NOT NULL);""")
    for _ in range(3):
        db.execute("INSERT INTO readings VALUES (NULL,'g','temperature','s','2026-11-02T14:02:58Z','x',24.7,'°C','ok','t')")
    db.commit(); db.close()
    monkeypatch.setenv("DATABASE_PATH", str(path))
    monkeypatch.syspath_prepend(str(CLOUD))
    sys.modules.pop("mqtt_store", None)
    mod = importlib.import_module("mqtt_store")
    assert mod.initialize_database() == "delete"
    with mod.connect_db() as db:
        assert db.execute("SELECT COUNT(*) FROM readings").fetchone()[0] == 1


def test_collector_healthcheck(tmp_path):
    env = {**os.environ, "COLLECTOR_HEARTBEAT": str(tmp_path / "hb")}
    run = lambda: subprocess.run([sys.executable, str(CLOUD / "collector.py"), "--health"], env=env).returncode
    assert run() == 1
    (tmp_path / "hb").touch()
    assert run() == 0
    old = time.time() - 300
    os.utime(tmp_path / "hb", (old, old))
    assert run() == 1


def test_streamlit_with_external_collector_hint(store):
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(CLOUD / "streamlit_app.py"), default_timeout=30).run()
    assert not at.exception, at.exception
    assert any("Collector-Dienst" in i.value for i in at.info)
