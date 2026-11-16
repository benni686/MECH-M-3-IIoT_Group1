"""MQTT-Collector als eigener Dienst.

Abonniert iiot/group/# am Kurs-Broker und schreibt alle Messwerte in SQLite,
unabhaengig davon, ob gerade jemand das Streamlit- oder Grafana-Dashboard offen hat.

Start lokal:   python collector.py
Healthcheck:   python collector.py --health   (Exit-Code 0 = verbunden)
"""
import logging
import os
import signal
import sqlite3
import sys
import threading
import time
from contextlib import closing
from pathlib import Path

HEARTBEAT = Path(os.getenv("COLLECTOR_HEARTBEAT", "/tmp/collector_heartbeat"))
LOG_EVERY_SECONDS = int(os.getenv("COLLECTOR_LOG_EVERY", "60"))


def health() -> int:
    """Healthy when the collector reported a live broker connection recently."""
    try:
        age = time.time() - HEARTBEAT.stat().st_mtime
    except FileNotFoundError:
        return 1
    return 0 if age < 90 else 1


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log = logging.getLogger("iiot-dashboard")

    from mqtt_store import DATABASE, MQTT_HOST, MQTT_PORT, MqttCollector, connect_db

    log.info("Collector startet: Broker %s:%s, Datenbank %s", MQTT_HOST, MQTT_PORT, DATABASE)
    collector = MqttCollector()

    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    signal.signal(signal.SIGINT, lambda *_: stop.set())

    last_log = 0.0
    while not stop.wait(5):
        if collector.connected:
            HEARTBEAT.touch()
        if time.monotonic() - last_log >= LOG_EVERY_SECONDS:
            last_log = time.monotonic()
            try:
                with closing(connect_db()) as db:
                    rows = db.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
            except sqlite3.Error as error:
                rows = f"? ({error})"
            ago = (
                f"{time.time() - collector.last_message_at:.0f} s"
                if collector.last_message_at else "noch keine"
            )
            log.info(
                "Status: broker=%s, letzte Nachricht vor %s, Messwerte in DB=%s%s",
                "verbunden" if collector.connected else "getrennt", ago, rows,
                f", Fehler={collector.last_error}" if collector.last_error else "",
            )

    log.info("Collector wird beendet")
    collector.stop()


if __name__ == "__main__":
    if "--health" in sys.argv:
        sys.exit(health())
    main()
