# Industrial Internet of Things (MECH-M-DUAL-3-IOT)

Unterlagen, Aufgabenstellung und Vorlagen für die synchronen Termine 1–3 der Lehrveranstaltung Industrial Internet of Things am MCI (WS 2026).

**Website:** https://jhumci.github.io/MECH-M-3-IIoT/

## Struktur

- `index.qmd`, `docs/`: Aufgabenstellung und Inhalte der Termine (Quarto)
- `docs/iot-specs/`: verbindliche Spezifikationen (`conventions.md`, `asyncapi.yaml`, `openapi.yaml`)
- `src/raspi_firmware/`: Vorlage für den Raspberry Pi Pico W (CircuitPython)
- `src/esp32_firmware/`: ESP32-C3-Firmware (PlatformIO/Arduino) für DHT20 und
  zwei analoge Hygrometer
- `docs/Dokumentation.qmd`: Platz für Ihre eigene Dokumentation

## ESP32-C3-Firmware

Die produktive Firmware liegt in `src/esp32_firmware/`. Sie verwendet:

- DHT20 an SDA `GPIO 5` und SCL `GPIO 6`
- Hygrometer 1 an `GPIO 0`/`A0`
- Hygrometer 2 an `GPIO 1`
- WLAN `ZentrumPRA-2`
- den Kurs-MQTT-Broker gemäß `docs/iot-specs/conventions.md`

Vor dem Flashen muss `.env.example` nach `.env` kopiert und mit den lokalen
WLAN-/MQTT-Zugangsdaten befüllt werden. Zusätzlich ist in
`src/esp32_firmware/src/main.cpp` der tatsächliche Gruppen-Slug einzutragen.
Die `.env` bleibt durch `.gitignore` lokal. Der Build wird aus dem
Firmware-Ordner gestartet:

```bash
pio run
pio run -t upload
pio device monitor --baud 115200
```

Die Firmware bietet außerdem `GET /config`, `POST /config` und `GET /status`
über die lokale IP-Adresse des ESP32 an.

## Dokumentation lokal bauen

```bash
pdm install
pdm run quarto preview
```

Bei jedem Push auf `main` wird die Website automatisch per GitHub Action gebaut und veröffentlicht (`.github/workflows/publish.yml`).
