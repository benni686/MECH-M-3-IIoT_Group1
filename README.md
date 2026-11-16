# Industrial Internet of Things (MECH-M-DUAL-3-IOT)

Unterlagen, Aufgabenstellung und Vorlagen für die synchronen Termine 1–3 der Lehrveranstaltung Industrial Internet of Things am MCI (WS 2026).

**Website:** https://jhumci.github.io/MECH-M-3-IIoT/

## Struktur

- `index.qmd`, `docs/`: Aufgabenstellung und Inhalte der Termine (Quarto)
- `docs/iot-specs/`: verbindliche Spezifikationen (`conventions.md`, `asyncapi.yaml`, `openapi.yaml`)
- `src/raspi_firmware/`: Vorlage für den Raspberry Pi Pico W (CircuitPython)
- `src/esp32_firmware/`: ESP32-C3-Firmware (PlatformIO/Arduino) für DHT20 und
  zwei analoge Hygrometer
- `src/cloud/`: MQTT-Aufnahme, SQLite-Datenhaltung und Web-Dashboard
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

## Streamlit-Dashboard

Im Repository-Stamm `.env.example` nach `.env` kopieren, das Kurs-Passwort
eintragen und starten:

```bash
docker compose up --build
```

Das Dashboard ist anschließend unter `http://localhost:8080` erreichbar.
Es speichert alle Nachrichten unter `iiot/group/+/sensor/+/state` in SQLite
und bietet Dropdowns für Gruppe, Sensoren und Zeitraum. Der MQTT-Collector
akzeptiert neben dem spezifizierten Standardformat auch die auf dem Kurs-Broker
beobachteten Payloads ohne Zeitstempel und kombinierte Temperatur-/Feuchtewerte.

## Dokumentation lokal bauen

```bash
pdm install
pdm run quarto preview
```

Bei jedem Push auf `main` wird die Website automatisch per GitHub Action gebaut und veröffentlicht (`.github/workflows/publish.yml`).
