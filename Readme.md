# Modulbeschreibung: Industrial Internet of Things (IIoT)

## Device Firmware

Startpunkte für die Firmware der IoT Devices finden sich in den Ordnern [`esp32_firmware`](./esp32:firmware) (ESP32 mit Plattformio) und [`raspi_pi_w_firmware`](./raspi_pi_w_firmware) (Raspberry Pi Pico W) mit MicroPython.


## Kommunikationsprotokolle

Die Allgemeinen Konventionen für die Kommunikation via MQTT und REST-API sind in [iot-specs/conventions.md](./iot-specs/conventions.md) beschrieben.

### MQTT Spezifikationen

Für die MQTT Kommunikation sind die Topics und Payloads in [iot-specs/asyncapi.yaml](./iot-specs/asyncapi.yaml) mittels AsyncAPI spezifiziert.

### REST API Spezifikationen

Für die REST API sind die Endpoints und Payloads in [iot-specs/openapi.yaml](./iot-specs/openapi.yaml) mittels OpenAPI spezifiziert.

Die Dokumentation der REST API kann heir gerendert eingesehen werden:
[![API Docs](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/jhumci/MECH-M-3-IIoT/refs/heads/main/iot-specs/openapi.yaml)](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/jhumci/MECH-M-3-IIoT/refs/heads/main/iot-specs/openapi.yaml)


## Backend

