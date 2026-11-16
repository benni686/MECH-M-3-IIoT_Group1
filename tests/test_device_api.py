"""Run with DEVICE_BASE_URL=http://<esp32-ip> pytest tests/test_device_api.py -v."""
import os
import pytest
import requests

BASE_URL = os.getenv("DEVICE_BASE_URL")
pytestmark = pytest.mark.skipif(not BASE_URL, reason="DEVICE_BASE_URL is not set")


def test_root_is_reachable():
    assert requests.get(f"{BASE_URL}/", timeout=3).status_code == 200


def test_config_round_trip():
    original = requests.get(f"{BASE_URL}/config", timeout=3).json()
    response = requests.post(f"{BASE_URL}/config", json={"reading_interval_seconds": 10}, timeout=3)
    assert response.status_code == 200
    assert requests.get(f"{BASE_URL}/config", timeout=3).json()["reading_interval_seconds"] == 10
    requests.post(f"{BASE_URL}/config", json={"reading_interval_seconds": original["reading_interval_seconds"]}, timeout=3).raise_for_status()


@pytest.mark.parametrize("body", ["not-json", "{}", '{"reading_interval_seconds":1}', '{"reading_interval_seconds":10,"unknown":true}'])
def test_invalid_config_is_rejected(body):
    response = requests.post(f"{BASE_URL}/config", data=body, headers={"Content-Type": "application/json"}, timeout=3)
    assert response.status_code == 400


def test_status_schema():
    response = requests.get(f"{BASE_URL}/status", timeout=3)
    assert response.status_code == 200
    required = {"device_id", "wifi_connected", "mqtt_connected", "clock_synchronized", "ip", "uptime_seconds", "last_publish_successful", "last_readings"}
    assert required <= response.json().keys()


def test_unknown_path_and_wrong_method():
    assert requests.get(f"{BASE_URL}/does-not-exist", timeout=3).status_code == 404
    response = requests.put(f"{BASE_URL}/config", timeout=3)
    assert response.status_code == 405
    assert "GET" in response.headers["Allow"] and "POST" in response.headers["Allow"]

