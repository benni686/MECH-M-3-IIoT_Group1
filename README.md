# Industrial Internet of Things (MECH-M-DUAL-3-IOT)

Unterlagen, Aufgabenstellung und Vorlagen für die synchronen Termine 1–3 der Lehrveranstaltung Industrial Internet of Things am MCI (WS 2026).

**Website:** https://jhumci.github.io/MECH-M-3-IIoT/

## Struktur

- `index.qmd`, `docs/`: Aufgabenstellung und Inhalte der Termine (Quarto)
- `docs/iot-specs/`: verbindliche Spezifikationen (`conventions.md`, `asyncapi.yaml`, `openapi.yaml`)
- `src/raspi_firmware/`: Vorlage für den Raspberry Pi Pico W (CircuitPython)
- `src/esp32_firmware/`: ESP32-C3-Firmware (PlatformIO/Arduino) für DHT20 und
  zwei analoge Hygrometer
- `src/cloud/`: MQTT-Collector, SQLite-Datenhaltung und Streamlit-Dashboard
- `grafana/`: Grafana-Datenquelle und -Dashboard (Provisioning)
- `tests/`: automatisierte Cloud- und ESP32-REST-API-Tests
- `docs/Dokumentation.qmd`: Platz für Ihre eigene Dokumentation

## ESP32-C3-Firmware

Die produktive Firmware liegt in `src/esp32_firmware/`. Sie verwendet:

- DHT20 an SDA `GPIO 8` und SCL `GPIO 9`
- Hygrometer 1 an `GPIO 0`/`A0`
- Hygrometer 2 an `GPIO 1`
- ein über die lokale `.env` konfiguriertes WLAN
- den Kurs-MQTT-Broker gemäß `docs/iot-specs/conventions.md`

Vor dem Flashen muss `.env.example` nach `.env` kopiert und mit den lokalen
WLAN-/MQTT-Zugangsdaten befüllt werden. Der Gruppen-Slug ist
`unterhuber-brachmann-reimeir-noessing`.
Die `.env` bleibt durch `.gitignore` lokal. Der Build wird aus dem
Firmware-Ordner gestartet:

```bash
pio run
pio run -t upload
pio device monitor --baud 115200
```

Die Firmware bietet außerdem `GET /config`, `POST /config` und `GET /status`
über die lokale IP-Adresse des ESP32 an.

## Cloud: Collector, Streamlit und Grafana

Im Repository-Stamm `.env.example` nach `.env` kopieren, das Kurs-Passwort
(`MQTT_PASSWORD`) eintragen und starten:

```bash
docker compose up --build
```

Es laufen drei Dienste auf einer gemeinsamen SQLite-Datenbank (Volume `iiot-data`):

| Dienst | Aufgabe | Adresse |
|---|---|---|
| `collector` | abonniert `iiot/group/#` und speichert alle Messwerte, auch wenn kein Dashboard offen ist | - |
| `dashboard` | Streamlit-Dashboard | http://localhost:8080 |
| `grafana` | Grafana-Dashboard "IIoT Sensor-Dashboard" (ohne Login lesbar, Admin: `admin` / `GRAFANA_ADMIN_PASSWORD`) | http://localhost:3000 |

Beide Dashboards bieten Auswahl von Gruppe, Sensoren und Zeitraum, aktuelle Werte,
Zeitverläufe je Einheit, Gerätestatus und die Rohdaten. Grafana nutzt das Plugin
`frser-sqlite-datasource`, das beim ersten Start automatisch installiert wird
(Internet nötig). Datenquelle und Dashboard liegen unter `grafana/` und werden
beim Start eingespielt; Änderungen in der Oberfläche gehen bei einem Neustart nicht
verloren, werden aber auch nicht in die JSON-Datei zurückgeschrieben.

Der Collector akzeptiert neben dem spezifizierten Standardformat auch die auf dem
Kurs-Broker beobachteten Payloads ohne Zeitstempel und kombinierte
Temperatur-/Feuchtewerte. Retained-Nachrichten werden bei jedem Neuverbinden
erneut zugestellt; doppelte Messwerte werden dabei verworfen.

Nützliche Befehle:

```bash
docker compose logs -f collector   # Verbindung und Anzahl gespeicherter Werte
docker compose ps                  # collector sollte "healthy" sein
docker compose down -v             # alles inkl. Daten löschen
```

## Dokumentation lokal bauen

```bash
pdm install
pdm run quarto preview
```

Bei jedem Push auf `main` wird die Website automatisch per GitHub Action gebaut und veröffentlicht (`.github/workflows/publish.yml`).
