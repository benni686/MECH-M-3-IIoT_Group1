"""Hermetic, non-secret configuration used by the automated tests."""

import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def test_settings(tmp_path_factory):
    root = Path(__file__).resolve().parents[1]
    private = tmp_path_factory.mktemp("config") / "settings.local.toml"
    private.write_text(
        """
[wifi.zentrum]
ssid = "test-wifi"
password = "test-password"

[broker.course]
password = "test-broker-password"

[grafana]
admin_password = "test-grafana-password"
""".lstrip(),
        encoding="utf-8",
    )
    previous_shared = os.environ.get("IIOT_SETTINGS_FILE")
    previous_private = os.environ.get("IIOT_LOCAL_SETTINGS_FILE")
    os.environ["IIOT_SETTINGS_FILE"] = str(root / "settings.toml")
    os.environ["IIOT_LOCAL_SETTINGS_FILE"] = str(private)
    yield
    if previous_shared is None:
        os.environ.pop("IIOT_SETTINGS_FILE", None)
    else:
        os.environ["IIOT_SETTINGS_FILE"] = previous_shared
    if previous_private is None:
        os.environ.pop("IIOT_LOCAL_SETTINGS_FILE", None)
    else:
        os.environ["IIOT_LOCAL_SETTINGS_FILE"] = previous_private
