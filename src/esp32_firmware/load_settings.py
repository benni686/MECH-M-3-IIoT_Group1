"""PlatformIO pre-build hook: generate firmware macros from shared TOML settings."""

import os
import tomllib
from copy import deepcopy

Import("env")


def merge(base, override):
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def read_toml(path, required=True):
    if not os.path.isfile(path):
        if required:
            raise SystemExit(f"Konfigurationsdatei fehlt: {path}")
        return {}
    try:
        with open(path, "rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise SystemExit(f"Konfiguration kann nicht gelesen werden: {path}: {error}")


project_dir = env.subst("$PROJECT_DIR")
repo_root = os.path.abspath(os.path.join(project_dir, "..", ".."))
settings = merge(
    read_toml(os.path.join(repo_root, "settings.toml")),
    read_toml(os.path.join(repo_root, "settings.local.toml")),
)

wifi_root = settings.get("wifi", {})
wifi_profile = wifi_root.get("active")
wifi = wifi_root.get(wifi_profile, {}) if isinstance(wifi_profile, str) else {}
broker_root = settings.get("broker", {})
broker_profile = broker_root.get("active")
broker = broker_root.get(broker_profile, {}) if isinstance(broker_profile, str) else {}
project = settings.get("project", {})
device = settings.get("device", {})

selected = {
    "WIFI_SSID": wifi.get("ssid"),
    "WIFI_PASSWORD": wifi.get("password"),
    "WIFI_PROFILE_NAME": wifi_profile,
    "MQTT_BROKER_HOST": broker.get("host"),
    "MQTT_BROKER_PORT": broker.get("port"),
    "MQTT_USER": broker.get("username"),
    "MQTT_PASSWORD": broker.get("password"),
    "MQTT_USE_TLS": broker.get("tls"),
    "MQTT_PROFILE_NAME": broker_profile,
    "MQTT_GROUP_SLUG": project.get("group_slug"),
    "DEVICE_IDENTIFIER": device.get("id"),
    "DEVICE_LOCATION": device.get("location"),
    "READING_INTERVAL_SECONDS": device.get("reading_interval_seconds"),
}

missing = [key for key, value in selected.items() if value is None or value == ""]
if missing:
    raise SystemExit("Fehlende Firmware-Konfiguration: " + ", ".join(missing))
if isinstance(selected["MQTT_BROKER_PORT"], bool) or not isinstance(
    selected["MQTT_BROKER_PORT"], int
) or not 1 <= selected["MQTT_BROKER_PORT"] <= 65535:
    raise SystemExit("MQTT-Broker-Port muss zwischen 1 und 65535 liegen.")
interval = selected["READING_INTERVAL_SECONDS"]
if isinstance(interval, bool) or not isinstance(interval, int) or not 2 <= interval <= 86400:
    raise SystemExit("reading_interval_seconds muss zwischen 2 und 86400 liegen.")

generated_dir = os.path.join(env.subst("$BUILD_DIR"), "generated")
os.makedirs(generated_dir, exist_ok=True)
header_file = os.path.join(generated_dir, "settings_config.h")
lines = ["#pragma once", "// Generated from settings.toml; never commit this file."]
for macro, value in selected.items():
    if isinstance(value, bool):
        value = "true" if value else "false"
    else:
        value = str(value)
    if ')CFG"' in value:
        raise SystemExit(f"Ungültige Zeichenfolge in {macro}")
    lines.append(f'#define {macro} R"CFG({value})CFG"')

with open(header_file, "w", encoding="utf-8", newline="\n") as header:
    header.write("\n".join(lines) + "\n")

env.Append(CPPPATH=[generated_dir])
