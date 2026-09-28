# Pre-Build-Skript für PlatformIO:
# Liest die Datei .env (Kopie von .env.example) und übergibt die Werte
# als C-Makros an den Compiler, z.B. WIFI_SSID -> #define WIFI_SSID "..."
import os

Import("env")

# Name in .env -> Name des Makros im Code
KEYS = {
    "WIFI_SSID": "WIFI_SSID",
    "WIFI_PASSWORD": "WIFI_PASSWORD",
    "MQTT_HOST": "MQTT_BROKER_HOST",
    "MQTT_USER": "MQTT_USER",
    "MQTT_PASSWORD": "MQTT_PASSWORD",
}

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

missing = [key for key in KEYS if key not in values]
if missing:
    raise SystemExit("In .env fehlen: " + ", ".join(missing))

env.Append(CPPDEFINES=[(macro, env.StringifyMacro(values[key])) for key, macro in KEYS.items()])
