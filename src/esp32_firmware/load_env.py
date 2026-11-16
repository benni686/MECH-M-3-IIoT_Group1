# Pre-Build-Skript für PlatformIO:
# Liest die Datei .env (Kopie von .env.example) und übergibt die Werte
# als C-Makros an den Compiler, z.B. WIFI_SSID -> #define WIFI_SSID "..."
import os

Import("env")

env_file = os.path.join(env.subst("$PROJECT_DIR"), ".env")
if not os.path.isfile(env_file):
    raise SystemExit("Datei .env fehlt: Kopieren Sie .env.example nach .env und tragen Sie Ihre Daten ein.")

values = {}
with open(env_file, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

wifi_profile = os.getenv("WIFI_PROFILE", values.get("WIFI_PROFILE", "zentrum")).lower()
mqtt_profile = os.getenv("MQTT_PROFILE", values.get("MQTT_PROFILE", "emqx")).lower()

if wifi_profile == "zentrum":
    selected_wifi = {
        "WIFI_SSID": values.get("WIFI_SSID"),
        "WIFI_PASSWORD": values.get("WIFI_PASSWORD"),
        "WIFI_PROFILE_NAME": "zentrum",
    }
elif wifi_profile == "kurs":
    selected_wifi = {
        "WIFI_SSID": values.get("KURS_SSID"),
        "WIFI_PASSWORD": values.get("KURS_PASSWORD"),
        "WIFI_PROFILE_NAME": "kurs",
    }
else:
    raise SystemExit('WIFI_PROFILE muss "zentrum" oder "kurs" sein.')

if mqtt_profile == "emqx":
    selected_mqtt = {
        "MQTT_BROKER_HOST": values.get("MQTT_HOST"),
        "MQTT_USER": values.get("MQTT_USER"),
        "MQTT_PASSWORD": values.get("MQTT_PASSWORD"),
        "MQTT_USE_TLS": values.get("MQTT_USE_TLS", "true"),
        "MQTT_PROFILE_NAME": "emqx",
    }
elif mqtt_profile == "kurs":
    selected_mqtt = {
        "MQTT_BROKER_HOST": "158.180.44.197",
        "MQTT_USER": "bobm",
        "MQTT_PASSWORD": values.get("MQTT_KURS_BROKER_PASS"),
        "MQTT_USE_TLS": "false",
        "MQTT_PROFILE_NAME": "kurs",
    }
else:
    raise SystemExit('MQTT_PROFILE muss "emqx" oder "kurs" sein.')

selected = {**selected_wifi, **selected_mqtt}
missing = [macro for macro, value in selected.items() if value is None or value == ""]
if missing:
    raise SystemExit(
        f'Für WIFI_PROFILE="{wifi_profile}" / MQTT_PROFILE="{mqtt_profile}" fehlen: '
        + ", ".join(missing)
    )

# Do not pass secrets as -D flags: shell metacharacters in passwords (for
# example '$' or '&') would corrupt the compiler command. Generate a header in
# PlatformIO's ignored build directory and force-include it in every unit.
generated_dir = os.path.join(env.subst("$BUILD_DIR"), "generated")
os.makedirs(generated_dir, exist_ok=True)
header_file = os.path.join(generated_dir, "env_config.h")

lines = ["#pragma once", "// Generated from .env; never commit this file."]
for macro, value in selected.items():
    if ')ENV"' in value:
        raise SystemExit(f"Ungültige Zeichenfolge in {macro}")
    lines.append(f'#define {macro} R"ENV({value})ENV"')

with open(header_file, "w", encoding="utf-8", newline="\n") as header:
    header.write("\n".join(lines) + "\n")

env.Append(CPPPATH=[generated_dir])
