# Vollständige Repository-Quelle: MECH-M-3-IIoT

Konsolidierter Stand aller textuellen Projektdateien. Lokale Geheimnisse, Binärbilder, Git-, IDE-, Build- und Lock-Artefakte sind ausgeschlossen.

## Enthaltene Dateien

- `.env.example`
- `.github/workflows/publish.yml`
- `.github/workflows/validate-asyncapi.yaml`
- `.gitignore`
- `README.md`
- `_quarto.yml`
- `docker-compose.yml`
- `docs/Dokumentation.qmd`
- `docs/Materialien.qmd`
- `docs/Termin_1_Grundkonzepte_IoT.qmd`
- `docs/Termin_2_Netzwerke.qmd`
- `docs/Termin_3_Cloud.qmd`
- `docs/iot-specs/asyncapi.yaml`
- `docs/iot-specs/conventions.md`
- `docs/iot-specs/openapi.yaml`
- `index.qmd`
- `pyproject.toml`
- `src/cloud/Dockerfile`
- `src/cloud/app.py`
- `src/cloud/requirements.txt`
- `src/esp32_firmware/.env.example`
- `src/esp32_firmware/.gitignore`
- `src/esp32_firmware/README.md`
- `src/esp32_firmware/config.h`
- `src/esp32_firmware/include/config_secure.h`
- `src/esp32_firmware/load_env.py`
- `src/esp32_firmware/platformio.ini`
- `src/esp32_firmware/src/Sensor.h`
- `src/esp32_firmware/src/main.cpp`
- `src/esp32_firmware/src/sensors/my_sensor.h`
- `src/raspi_firmware/code.py`
- `src/raspi_firmware/lib/toml.py`
- `src/raspi_firmware/settings.toml`
- `tests/requirements.txt`
- `tests/test_cloud.py`
- `tests/test_device_api.py`

## Bild-Assets

- `docs/images/BrokerSequence.png`
- `docs/images/IoTNetwork.svg`
- `docs/images/pico_dht11_wiring.svg`
- `docs/images/raspberry_pi_Pico-R3-Pinout-narrow.png`

---

# Datei: `.env.example`

```dotenv
MQTT_HOST=158.180.44.197
MQTT_PORT=1883
MQTT_USER=bobm
MQTT_PASSWORD=In Vorlesung erfragen
MQTT_TLS=false
```

---

# Datei: `.github/workflows/publish.yml`

```yaml
on:
  workflow_dispatch:
  push:
    branches: main

name: Quarto Publish

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
        
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install jupyter nbformat pandas matplotlib # add other packages your notebooks need

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Render and Publish
        uses: quarto-dev/quarto-actions/publish@v2
        with:
          target: gh-pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

# Datei: `.github/workflows/validate-asyncapi.yaml`

```yaml
name: Validate AsyncAPI Spec

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/iot-specs/asyncapi.yaml'
      - '.github/workflows/validate-asyncapi.yaml'
  pull_request:
    paths:
      - 'docs/iot-specs/asyncapi.yaml'
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install AsyncAPI CLI
        run: npm install -g @asyncapi/cli
      - name: Validate asyncapi.yaml
        run: asyncapi validate docs/iot-specs/asyncapi.yaml
```

---

# Datei: `.gitignore`

```gitignore
.vscode/
.venv/
*.pyc
__pycache__/
.pdm-python
/.quarto/
_site/
# PlatformIO / Zugangsdaten
.pio/
.env
*.sqlite3
.pytest_cache/

**/*.quarto_ipynb
```

---

# Datei: `README.md`

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

## Cloud-Dashboard

Im Repository-Stamm `.env.example` nach `.env` kopieren, das Kurs-Passwort
eintragen und starten:

```bash
docker compose up --build
```

Das Dashboard ist anschließend unter `http://localhost:8080` erreichbar.

## Dokumentation lokal bauen

```bash
pdm install
pdm run quarto preview
```

Bei jedem Push auf `main` wird die Website automatisch per GitHub Action gebaut und veröffentlicht (`.github/workflows/publish.yml`).

---

# Datei: `_quarto.yml`

```yaml
project:
  type: website
  title: "Industrial Internet of Things"
  output-dir: _site
  resources:
    - docs/iot-specs/asyncapi.yaml
    - docs/iot-specs/openapi.yaml
    - docs/iot-specs/conventions.md
    - src/raspi_firmware/settings.toml
    - src/raspi_firmware/code.py


website:
  title: "Industrial Internet of Things"
  reader-mode: true
  page-footer:
    left: Industrial Internet of Things WS 2026 (MECH-M-DUAL-3-IOT)
    center: "[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) Julian Huber"
    right: This book was built with <a href="https://quarto.org/">Quarto</a>.
  site-url: https://github.com/jhumci/MECH-M-3-IIoT
  repo-url: https://github.com/jhumci/MECH-M-3-IIoT
  repo-branch: main
  repo-actions: [edit, issue]
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: docs/Materialien.qmd
        text: Materialien
      - href: docs/Termin_1_Grundkonzepte_IoT.qmd
        text: Termin 1 Grundkonzepte IoT
      - href: docs/Termin_2_Netzwerke.qmd
        text: Termin 2 Netzwerke
      - href: docs/Termin_3_Cloud.qmd
        text: Termin 3 Cloud
      - href: docs/Dokumentation.qmd
        text: Eigene Dokumentation

format:
  html:
    theme: cosmo
    toc: true
```

---

# Datei: `docker-compose.yml`

```yaml
services:
  dashboard:
    build: ./src/cloud
    restart: unless-stopped
    environment:
      MQTT_HOST: ${MQTT_HOST:-158.180.44.197}
      MQTT_PORT: ${MQTT_PORT:-1883}
      MQTT_USER: ${MQTT_USER:-bobm}
      MQTT_PASSWORD: ${MQTT_PASSWORD:?MQTT_PASSWORD must be set in the root .env file}
      MQTT_TLS: ${MQTT_TLS:-false}
      DATABASE_PATH: /data/iiot.sqlite3
    ports:
      - "8080:8080"
    volumes:
      - iiot-data:/data
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"]
      interval: 30s
      timeout: 5s
      retries: 3

volumes:
  iiot-data:
```

---

# Datei: `docs/Dokumentation.qmd`

# Projektdokumentation Gruppe 1

## Team und Ziel

**Unterhuber, Brachmann, Reimeir und Noessing** entwickeln eine IIoT-Lösung zur Überwachung von Temperatur, Luftfeuchtigkeit und zwei Hygrometern. Ein ESP32-C3 erfasst die Werte, sendet sie über MQTT und bietet lokal eine REST-API. Eine containerisierte Anwendung speichert alle Gruppen automatisch in SQLite und stellt sie in einem Dashboard dar.

Der Gruppen-Slug ist `unterhuber-brachmann-reimeir-noessing`.

## Architektur

1. Der ESP32-C3 liest DHT20 und zwei analoge Hygrometer.
2. NTP stellt UTC-Zeitstempel bereit.
3. Messwerte und Gerätestatus werden über MQTT veröffentlicht.
4. Der ESP32 stellt parallel die lokale HTTP-API bereit.
5. Der Cloud-Container abonniert Wildcard-Topics, persistiert Daten in SQLite und stellt Dashboard und JSON-API auf Port 8080 bereit.

## Hardware und Verkabelung

| Komponente | ESP32-C3-Pin | Funktion |
|---|---:|---|
| DHT20 SDA | GPIO 8 | I²C-Daten |
| DHT20 SCL | GPIO 9 | I²C-Takt |
| Hygrometer 1 | GPIO 0 | Analogsignal |
| Hygrometer 2 | GPIO 1 | Analogsignal |
| Sensorversorgung | 3,3 V | Versorgung |
| Sensormasse | GND | gemeinsame Masse |

Analoge Signale dürfen 3,3 V nicht überschreiten. Die Kalibrierwerte stehen in `src/esp32_firmware/src/main.cpp`.

## Mikrocontroller einrichten

Voraussetzungen sind VS Code, PlatformIO und ein per USB angeschlossener ESP32-C3.

```bash
cd src/esp32_firmware
cp .env.example .env
# WLAN und Kurs-Broker-Passwort in .env eintragen
pio run
pio run -t upload
pio device monitor --baud 115200
```

Die `.env` ist ignoriert und darf nicht committed werden. Die serielle Ausgabe zeigt WLAN-IP, I²C-Erkennung, MQTT-Verbindung und Publish-Ergebnisse. Vor einem Messversand wartet die Firmware auf eine gültige NTP-Uhr.

### WLAN- und Brokerprofile

In `.env` lassen sich WLAN und Broker unabhängig auswählen:

```text
WIFI_PROFILE="zentrum"  # oder "kurs"
MQTT_PROFILE="emqx"     # oder "kurs"
```

Das Zentrum-Profil liest `WIFI_SSID` und `WIFI_PASSWORD`, das Kursprofil
`KURS_SSID` und `KURS_PASSWORD`. Das EMQX-Profil liest `MQTT_HOST`,
`MQTT_USER`, `MQTT_PASSWORD` und `MQTT_USE_TLS`. Für das Kurs-Brokerprofil
werden `158.180.44.197:1883`, Benutzer `bobm` und unverschlüsseltes MQTT
automatisch gesetzt; einzutragen ist nur `MQTT_KURS_BROKER_PASS`.

## MQTT

Kurs-Broker: `158.180.44.197:1883`, Benutzer `bobm`, unverschlüsselt. Topics:

```text
iiot/group/unterhuber-brachmann-reimeir-noessing/sensor/temperature/state
iiot/group/unterhuber-brachmann-reimeir-noessing/sensor/humidity/state
iiot/group/unterhuber-brachmann-reimeir-noessing/sensor/hygrometer-1/state
iiot/group/unterhuber-brachmann-reimeir-noessing/sensor/hygrometer-2/state
iiot/group/unterhuber-brachmann-reimeir-noessing/status
```

```json
{"timestamp":"2026-11-02T10:00:00Z","sensor_id":"yourmuesli-innsbruck-01","value":22.5,"unit":"°C","status":"ok"}
```

Das Status-Topic wird retained gesendet. Beim Verbindungsaufbau wird `{"status":"offline"}` als Last Will hinterlegt; normale Zustände sind `ok` und `error`.

## REST-API des ESP32

Basis-URL: `http://<ESP32-IP>`. Die vollständige Spezifikation steht in `docs/iot-specs/openapi.yaml`.

| Methode | Pfad | Zweck |
|---|---|---|
| GET | `/` | Erreichbarkeit |
| GET | `/config` | Gerätekonfiguration lesen |
| POST | `/config` | Sendeintervall ändern |
| GET | `/status` | Verbindungen, Uptime, letzte Werte und Versandstatus |

```bash
curl http://<ESP32-IP>/config
curl -X POST http://<ESP32-IP>/config -H 'Content-Type: application/json' -d '{"reading_interval_seconds":10}'
curl http://<ESP32-IP>/status
```

Intervalle von 2 bis 86400 Sekunden sind zulässig. Die Änderung wirkt sofort, bleibt aber nach einem Neustart nicht erhalten. Ungültiges JSON liefert 400, unbekannte Pfade 404 und falsche Methoden 405.

## Tests

```bash
python -m pip install -r tests/requirements.txt
pytest tests/test_cloud.py -v
DEVICE_BASE_URL=http://<ESP32-IP> pytest tests/test_device_api.py -v
```

Ohne `DEVICE_BASE_URL` werden Hardwaretests übersprungen. Vor der Abgabe müssen sie am geflashten Gerät ausgeführt werden.

## Cloud-Lösung

Im Repository-Stamm:

```bash
cp .env.example .env
# Kurs-Broker-Passwort eintragen
docker compose up --build
```

- Dashboard: `http://localhost:8080/`
- Healthcheck: `http://localhost:8080/health`
- Statistik: `http://localhost:8080/api/sensors`
- Messwerte: `http://localhost:8080/api/readings?group=unterhuber-brachmann-reimeir-noessing&sensor=temperature`

Die Anwendung abonniert `iiot/group/+/sensor/+/state` und `iiot/group/+/status`. Neue Gruppen und Sensortypen erscheinen automatisch. SQLite liegt im Volume `iiot-data`. Das Dashboard zeigt Status, Anzahl, Minimum, Mittelwert, Maximum und Temperaturverlauf.

```bash
docker compose down
```

`docker compose down -v` löscht auch die Datenbank und darf nur bewusst verwendet werden.

## Empfehlungen für die IT-Abteilung

| Richtung/Ziel | Protokoll/Port | Zweck |
|---|---|---|
| ausgehend zu `158.180.44.197` | TCP 1883 | MQTT |
| ausgehend zu NTP-Servern | UDP 123 | UTC-Zeit |
| lokal zum ESP32 | TCP 80 | REST-API |

Laptop und ESP32 müssen für Konfiguration und Tests im selben Netz liegen; Client-Isolation in Gäste-WLANs verhindert dies. Port 80 darf wegen unverschlüsseltem HTTP nicht ins Internet freigegeben werden. Fernwartung sollte über ein authentifiziertes VPN erfolgen. MQTT 1883 ist ebenfalls unverschlüsselt; produktiv wären TLS, Zertifikatsprüfung, getrennte Gerätezugänge und minimale Broker-ACLs erforderlich.

## Fehlerbehebung

- **DHT20 fehlt:** Versorgung, GND, SDA GPIO 8, SCL GPIO 9 und Pull-ups prüfen.
- **Keine MQTT-Daten:** `.env`, Firewall, Broker und serielles Log prüfen.
- **Falsche Zeit:** UDP 123 und DNS freigeben.
- **REST nicht erreichbar:** IP, gleiches WLAN und Client-Isolation prüfen.
- **Dashboard leer:** `docker compose logs dashboard`, Passwort und Topics prüfen.
- **Hygrometer unplausibel:** ADC-Spannung und Trocken-/Nasskalibrierung prüfen.

## Relevante Dateien

- `src/esp32_firmware/src/main.cpp`
- `src/esp32_firmware/.env.example`
- `docs/iot-specs/openapi.yaml`
- `docs/iot-specs/asyncapi.yaml`
- `src/cloud/app.py`
- `docker-compose.yml`
- `tests/`

---

# Datei: `docs/Materialien.qmd`

# Materialien

Sie erhalten in der ersten Sitzung die folgenden Materialien ausgehändigt:

| Anzahl | Bauteil | Hinweis |
|---|---|---|
| 1 | Raspberry Pi Pico W (oder ESP32) | Mikrocontroller mit WLAN |
| 1 | Temperatursensor DHT11 | Temperatur und Luftfeuchtigkeit, 4 Pins |
| 1 | Widerstand 10 kΩ | Pull-up für die Datenleitung (Farbringe braun-schwarz-orange) |
| 1 | Steckbrett (Breadboard) | für den Aufbau ohne Löten |
| 3 | Steckkabel (Jumper Wires) | idealerweise rot, gelb/grün, schwarz |
| 1 | USB-Micro-B-Kabel (bei Bedarf) | Stromversorgung und Programmierung |

Bitte geben Sie diese nach Ende des Semesters unaufgefordert zurück, erst dann wird die Note freigegeben.

Der Einsatz anderer Hardware kann mit der Lehrveranstaltungsleitung abgesprochen werden.

# Aufbau der Hardware

Der DHT11 wird mit drei Leitungen an den Pico W angeschlossen: Versorgungsspannung (3,3 V), Masse (GND) und eine Datenleitung. Der 10 kΩ-Widerstand verbindet die Datenleitung mit 3,3 V (Pull-up), damit die Leitung im Ruhezustand einen definierten Pegel hat.

![Verdrahtung Raspberry Pi Pico W mit DHT11](images/pico_dht11_wiring.svg)

| Pico W | | DHT11 | Kabel |
|---|---|---|---|
| Pin 36 – 3V3(OUT) | → | Pin 1 – VCC | rot |
| Pin 29 – GP22 | → | Pin 2 – DATA | gelb |
| – | | Pin 3 – NC (nicht verbunden) | – |
| Pin 28 – GND | → | Pin 4 – GND | schwarz |

Zusätzlich: **10 kΩ-Widerstand** zwischen DHT11 Pin 1 (VCC) und Pin 2 (DATA).

### Schritt für Schritt

1. **USB-Kabel abstecken.** Verdrahten Sie immer im stromlosen Zustand.
2. **DHT11 einstecken.** Stecken Sie den Sensor so in das Steckbrett, dass jeder der vier Pins in einer eigenen Reihe steckt. Pin 1 ist der linke Pin, wenn das Gitter zu Ihnen zeigt und die Pins nach unten zeigen.
3. **Widerstand einstecken.** Verbinden Sie mit dem Widerstand die Reihe von Pin 1 (VCC) mit der Reihe von Pin 2 (DATA). Die Einbaurichtung ist beim Widerstand egal.
4. **Kabel stecken.** Verbinden Sie die Pins des Pico W mit den Reihen des Sensors wie in der Tabelle angegeben. Die Pin-Nummern finden Sie im [Pinout](images/raspberry_pi_Pico-R3-Pinout-narrow.png), Pin 1 ist neben dem USB-Anschluss markiert.
5. **Kontrolle.** Prüfen Sie vor dem Einstecken des USB-Kabels, dass 3,3 V und GND nicht vertauscht sind. Ein falsch gepolter Sensor kann heiß werden und kaputtgehen.
6. **In der Konfiguration eintragen.** Der Datenpin wird in der [`settings.toml`](https://github.com/jhumci/MECH-M-3-IIoT/blob/main/src/raspi_firmware/settings.toml) als `sensor_pin = 22` angegeben.

::: {.callout-tip}
## Hinweise
- **Steckbrett:** Die fünf Löcher einer Reihe (a–e) sind im Inneren leitend verbunden. Was in derselben Reihe steckt, ist also miteinander verbunden.
- **DHT11 als Modul:** Manche DHT11 sind auf einer kleinen Platine mit nur drei Pins verbaut. Dort ist der Pull-up-Widerstand bereits eingebaut und die Pin-Reihenfolge ist aufgedruckt (z.B. `+`, `out`, `-`). Der zusätzliche Widerstand entfällt dann.
- **ESP32:** Der Aufbau ist identisch (3V3, GND, Datenpin). Die ESP32-Vorlage nutzt GPIO 4 als Datenpin (`DHT_SENSOR_PIN` in `src/esp32_firmware/src/sensors/my_sensor.h`).
- **Keine Messwerte?** Der DHT11 liefert höchstens alle 1–2 Sekunden einen neuen Wert. Häufiges Auslesen führt zu Fehlern. Auch bei korrektem Aufbau schlägt gelegentlich eine Messung fehl (Checksum-Fehler), das ist normal und muss in der Firmware abgefangen werden.
- **Zu warm?** Der Pico W erwärmt sich im Betrieb, vor allem durch das WLAN-Modul. Sitzt der DHT11 direkt daneben, zeigt er einige Grad zu viel an. Ein paar Zentimeter Abstand, z.B. am anderen Ende des Steckbretts, helfen.
:::

---

# Datei: `docs/Termin_1_Grundkonzepte_IoT.qmd`

# Synchron

## [Grundbegriffe](https://jhumci.github.io/2024_SoSe_IoT1/IoT_1_Grundbegriffe/#)

![](images/IoTNetwork.svg)

## [Kommunikations-Architekturen (MQTT)](https://jhumci.github.io/2024_SoSe_IoT1/IoT_4_Architekturen/)

![](images/BrokerSequence.png)


## [Telemetrie](https://jhumci.github.io/2023_WiSe_IoT2/IoT_8_Telemetrie/)

![](images/raspberry_pi_Pico-R3-Pinout-narrow.png)


## Vorstellung der Aufgabenstellung

Jede Gruppe entwickelt mit einem eigenen Microcontroller und Sensor. Ziel des ersten Teils ist eine Firmware, die die Messwerte des DHT11 so an den Kurs-Broker sendet, wie es [`conventions.md`](https://github.com/jhumci/MECH-M-3-IIoT/blob/main/docs/iot-specs/conventions.md) und [`asyncapi.yaml`](https://github.com/jhumci/MECH-M-3-IIoT/blob/main/docs/iot-specs/asyncapi.yaml) vorgeben.

- [ ] Erstellen Sie einen Fork von diesem [Git-Repository](https://github.com/jhumci/MECH-M-3-IIoT) und laden Sie `Robo-Chris` ein.
- [ ] Verkabeln Sie den Sensor wie unter [Materialien](Materialien.qmd) beschrieben.
- [ ] Richten Sie den Pico W ein (siehe *Erste Schritte* unten) und arbeiten Sie die *Meilensteine* der Reihe nach ab. Für die ersten Meilensteine reicht ein einfaches Skript ohne Konfigurationsdatei und ohne Klassen.
- [ ] Überprüfen Sie mit dem [MQTT Explorer](https://mqtt-explorer.com/), ob Ihre Nachrichten auf dem richtigen Topic und im richtigen Format ankommen.
- [ ] Refactoren Sie Ihren Code in die Struktur der Vorlage [`code.py`](https://github.com/jhumci/MECH-M-3-IIoT/blob/main/src/raspi_firmware/code.py): alle veränderlichen Werte kommen in die [`settings.toml`](https://github.com/jhumci/MECH-M-3-IIoT/blob/main/src/raspi_firmware/settings.toml), die Logik in die vorgesehenen Klassen.

### Erste Schritte mit dem Pico W

::: {.callout-important}
## CircuitPython, nicht MicroPython
Die Vorlage `code.py`, der TOML-Parser in `lib/` und alle Hinweise auf dieser Seite beziehen sich auf **CircuitPython**. MicroPython ist ein naher Verwandter, aber die Vorlage und die Adafruit-Bibliotheken laufen dort nicht. Für den ESP32 gibt es eine eigene Vorlage in `src/esp32_firmware` (Arduino/PlatformIO). Wenn Sie MicroPython verwenden möchten, sprechen Sie das vorher mit der Lehrveranstaltungsleitung ab.
:::

1. **CircuitPython installieren.** Laden Sie die aktuelle `.uf2`-Datei für den [Raspberry Pi Pico W](https://circuitpython.org/board/raspberry_pi_pico_w/) herunter. Halten Sie die Taste `BOOTSEL` am Pico gedrückt, während Sie das USB-Kabel einstecken. Es erscheint ein Laufwerk `RPI-RP2`, auf das Sie die `.uf2`-Datei kopieren. Der Pico startet neu und meldet sich als Laufwerk `CIRCUITPY`.
2. **Bibliotheken kopieren.** Laden Sie das [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries) herunter, dessen Versionsnummer zu Ihrer CircuitPython-Version passt (z.B. Bundle 10.x für CircuitPython 10). Legen Sie auf `CIRCUITPY` einen Ordner `lib/` an und kopieren Sie aus dem Bundle hinein:

   | Datei / Ordner aus dem Bundle | Wofür |
   |---|---|
   | `adafruit_dht.mpy` | DHT11 auslesen |
   | `adafruit_minimqtt/` (ganzer Ordner) | MQTT-Client |
   | `adafruit_connection_manager.mpy`, `adafruit_ticks.mpy` | werden von MiniMQTT benötigt |
   | `adafruit_ntp.mpy` | Uhrzeit aus dem Internet holen (siehe Hinweise unten) |

   Dazu kommt `toml.py` aus [`src/raspi_firmware/lib/`](https://github.com/jhumci/MECH-M-3-IIoT/tree/main/src/raspi_firmware/lib) dieses Repositories.
3. **`code.py` und `settings.toml`** liegen im Hauptverzeichnis von `CIRCUITPY`. `code.py` startet automatisch, sobald Sie eine Datei auf dem Laufwerk speichern. Ein eigener Upload-Schritt ist nicht nötig.
4. **Serielle Konsole öffnen.** Alle `print()`-Ausgaben und alle Fehlermeldungen Ihres Programms erscheinen nur dort. Ohne Konsole arbeiten Sie blind. Geeignet sind z.B. der [Mu Editor](https://codewith.mu/), die Erweiterung *Serial Monitor* in VS Code, PuTTY (Windows) oder `screen`/`minicom` (Linux, macOS), jeweils mit 115200 Baud. Details: [Connecting to the Serial Console](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console). In der Konsole beendet `Ctrl+C` das Programm und `Ctrl+D` startet es neu.

### Meilensteine

Jeder Meilenstein liefert ein sichtbares Ergebnis. Gehen Sie erst zum nächsten, wenn der aktuelle stabil läuft, dann wissen Sie bei Problemen immer, welcher Teil schuld ist.

| # | Meilenstein | Woran Sie den Erfolg erkennen |
|---|---|---|
| 1 | LED blinken lassen (`board.LED`, `digitalio`) | Die Onboard-LED blinkt. Sie wissen, wie Sie Code auf den Pico bringen und die Konsole lesen. |
| 2 | Sensor auslesen (`adafruit_dht`), alle 2 Sekunden `print()` | Temperatur und Luftfeuchtigkeit erscheinen in der Konsole. Einzelne Fehlversuche werden abgefangen und das Programm läuft weiter. |
| 3 | Mit dem WLAN verbinden (`wifi`, `socketpool`) | Die IP-Adresse des Pico erscheint in der Konsole. |
| 4 | Eine einzelne MQTT-Nachricht senden (`adafruit_minimqtt`) | Die Nachricht ist im MQTT Explorer unter Ihrem Topic sichtbar. |
| 5 | Spezifikation erfüllen | Payload ist JSON mit `timestamp`, `value` und `unit` wie in `asyncapi.yaml`. Auf dem Status-Topic steht `ok`, nach dem Abstecken des Pico wechselt es nach kurzer Zeit von selbst auf `offline`. |
| 6 | Refactoring | Struktur wie in der Vorlage, Konfiguration in `settings.toml`, Sendeintervall aus der Konfiguration. |

### Hinweise zu den schwierigen Stellen

Hier keine Lösungen, sondern die Stichworte, die Ihnen die Suche verkürzen:

- **Zeitstempel.** Die Spezifikation verlangt einen Zeitstempel in UTC nach ISO 8601. Der Pico hat keine batteriegepufferte Uhr; nach dem Einschalten steht sie auf dem Jahr 2000. Stichworte: `adafruit_ntp` holt die Zeit aus dem Internet, das Modul `rtc` setzt die Uhr des Pico.
- **Datum formatieren.** Das `time`-Modul von CircuitPython hat kein `strftime`. `time.localtime()` liefert aber ein Tupel aus Jahr, Monat, Tag, Stunde, Minute und Sekunde, aus dem sich der String mit einer Formatierung zusammenbauen lässt.
- **Client-ID.** Der Broker erlaubt jede Client-ID nur einmal. Melden sich zwei Geräte mit derselben ID an, werfen sie sich gegenseitig hinaus, und beide sehen ständig Verbindungsabbrüche. Die Vorlage der `settings.toml` hat dafür keinen eigenen Schlüssel. Überlegen Sie, woraus Sie eine ID ableiten, die über alle Gruppen hinweg eindeutig ist.
- **Last Will.** Das `offline` auf dem Status-Topic sendet nicht Ihr Programm, sondern der Broker, wenn die Verbindung abbricht. Es wird beim Verbindungsaufbau hinterlegt. Stichwort: `will_set()` in MiniMQTT, retained.
- **Sensorfehler.** Der DHT11 liefert regelmäßig einen `RuntimeError` (Checksum, Timing). Das ist kein Fehler in Ihrem Aufbau, sondern normal. Fangen Sie ihn ab und versuchen Sie es beim nächsten Intervall erneut.

::: {.callout-warning collapse="true"}
## Typische Probleme
- **WLAN wird nicht gefunden.** Der Pico W kann nur 2,4-GHz-Netze. Viele Router senden 5 GHz unter demselben Namen; das erkennt der Pico nicht. Handy-Hotspots funktionieren meist, wenn sie auf 2,4 GHz eingestellt sind.
- **`ImportError: no module named 'socket'`** oder `select`: Diese Module gibt es in CircuitPython nicht. Für Netzwerkzugriffe ist `socketpool` zuständig, siehe Termin 2.
- **`AttributeError: 'module' object has no attribute 'strftime'`**: siehe Hinweis *Datum formatieren*.
- **`ImportError: no module named 'adafruit_...'`**: Datei fehlt in `lib/` oder das Bundle passt nicht zur CircuitPython-Version.
- **Temperatur zu hoch.** Sitzt der Sensor direkt neben dem Pico, misst er dessen Abwärme mit. Siehe [Materialien](Materialien.qmd).
- **Alles hängt nach mehreren Neustarts.** Häufige Neustarts per Speichern oder `Ctrl+D` können das WLAN-Modul aufhängen. USB-Kabel kurz abstecken, dann läuft es wieder.
- **Verbindung bricht ständig ab.** Meist eine doppelte Client-ID, siehe oben.
:::

# Asynchrone Inhalte

Mit folgenden Inhalten sollten Sie sich vertraut machen, um die Aufgabenstellung erfolgreich zu bearbeiten:

**CircuitPython auf dem Pico W** (die Vorlage baut darauf auf):

- [Welcome to CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython): Installation, `CIRCUITPY`-Laufwerk, serielle Konsole
- [Pico W WiFi with CircuitPython](https://learn.adafruit.com/pico-w-wifi-with-circuitpython): WLAN-Verbindung, `settings.toml`, erste Netzwerkzugriffe
- [MQTT in CircuitPython](https://learn.adafruit.com/mqtt-in-circuitpython): Einführung in MiniMQTT, dazu die [API-Dokumentation](https://docs.circuitpython.org/projects/minimqtt/en/latest/)
- [DHT CircuitPython Code](https://learn.adafruit.com/dht/dht-circuitpython-code): Auslesen des DHT11 mit `adafruit_dht`
- [Wokwi](https://wokwi.com/projects/new/micropython-pi-pico-w): Online-Simulator für Mikrocontroller. Nützlich, um Schaltungen zu testen; simuliert allerdings MicroPython, nicht CircuitPython.

**MQTT und Schnittstellen-Beschreibung:**

- [AWS Whitepaper on MQTT](https://docs.aws.amazon.com/whitepapers/latest/designing-mqtt-topics-aws-iot-core/mqtt-design-best-practices.html): Topic-Design und Best Practices
- [AsyncAPI](https://www.asyncapi.com/en): Die Spezifikation, in der `asyncapi.yaml` geschrieben ist. Im [AsyncAPI Studio](https://studio.asyncapi.com/) lässt sich die Datei lesbar darstellen.
- [MQTT Explorer](https://mqtt-explorer.com/): Freier MQTT-Client zur Visualisierung von Nachrichten. Abonnieren Sie `iiot/group/#`, um auch die Nachrichten der anderen Gruppen zu sehen.

**Zum Hintergrund** (nicht für die Vorlage nötig):

- [MicroPython](https://mciwing.github.io/micropython/) und die [MicroPython-Einführung](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html): der nahe Verwandte von CircuitPython, verbreitet auf dem ESP32
- [PlatformIO](https://docs.platformio.org/en/latest/): Build-System für die ESP32-Vorlage in `src/esp32_firmware`

---

# Datei: `docs/Termin_2_Netzwerke.qmd`

# Synchron

## [Netzwerke](https://jhumci.github.io/2024_SoSe_IoT1/IoT_5_Netzwerke/)
## [Kommunikations-Architekturen (REST)](https://jhumci.github.io/2024_SoSe_IoT1/IoT_4_Architekturen/)
## [Firewalls](https://jhumci.github.io/2023_WiSe_IoT2/IoT_6_SecuritySafety/#64-firewalls)

## Vorstellung der Aufgabenstellung

- [ ] Die Netzwerkkonfiguration (z.B. WLAN-Zugangsdaten) wird über eine Konfig-Datei [`settings.toml`](https://github.com/jhumci/MECH-M-3-IIoT/blob/main/src/raspi_firmware/settings.toml) bereitgestellt, die der Microcontroller beim Start einliest.
- [ ] Der Microcontroller hat zwei HTTP-Endpunkte (unverschlüsselt), die JSON senden und empfangen:
  - `/config` (GET, POST): Zum Abrufen und Setzen der Konfiguration (z.B. Sendeintervall).
  - `/status` (GET): Zum Abrufen des aktuellen Status des Geräts (z.B. letzte gesendete Werte, Verbindungsstatus, Uptime).
- [ ] Die Schnittstellen sind in der OpenAPI Specification dokumentiert, siehe [`openapi.yaml`](https://github.com/jhumci/MECH-M-3-IIoT/blob/main/docs/iot-specs/openapi.yaml) und [`conventions.md`](https://github.com/jhumci/MECH-M-3-IIoT/blob/main/docs/iot-specs/conventions.md). Dort ist bisher nur `/config` beschrieben.
- [ ] Einigen Sie sich in der Gesamtgruppe auf die Felder von `/status` und auf alle weiteren Felder von `/config`, die alle Sensoren unterstützen müssen, **bis vor dem 3. Synchron-Termin**. Vorgehen: Eine Gruppe stellt einen Pull Request gegen `docs/iot-specs/openapi.yaml` im Original-Repository mit einem Vorschlag. Die anderen Gruppen kommentieren dort. Was vor dem 3. Termin gemerged ist, gilt für alle.
- [ ] Schreiben Sie Testfälle, mit denen sich die HTTP-API Ihres Geräts überprüfen lässt, und legen Sie diese im Repository ab (z.B. unter `tests/`). Welches Werkzeug Sie dafür verwenden, hat Auswirkung auf die Bewertung: [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) in VS Code (*befriedigend*), `unittest` oder `pytest` in Python (*gut*), oder das OpenAPI-Tooling, z.B. [Schemathesis](https://schemathesis.readthedocs.io/) oder [Swagger Codegen](https://swagger.io/tools/swagger-codegen/) (*sehr gut*). Wie die Testfälle ausgeführt werden, sollte in der Dokumentation beschrieben sein.
- [ ] Gehen Sie davon aus, dass Sie an allen Standorten Zugriff auf ein WLAN haben, welches durch eine externe Firewall geschützt ist (Whitelist). Schreiben Sie einen kurzen Absatz für Ihre Dokumentation, worauf die örtliche IT-Abteilung achten muss, wenn sie Ihre Geräte in das Netzwerk integriert, damit die Daten auch wirklich beim MQTT-Broker ankommen. Diskutieren Sie auch, wie Sie die HTTP-API aus der Ferne zugänglich machen können und welche Gefahren und Hindernisse bestehen.

### Vorgehen

Bauen Sie die HTTP-Schnittstelle in dieser Reihenfolge auf und testen Sie jeden Schritt von Ihrem Laptop aus, bevor Sie den nächsten beginnen. Laptop und Pico müssen dazu im selben WLAN sein.

1. **Ein fester Text auf `GET /`.** Der Server nimmt eine Verbindung an, liest die Anfrage, antwortet mit `HTTP/1.1 200 OK`, einer Leerzeile und einem beliebigen Text. Das prüfen Sie mit `curl`, das auf Windows, macOS und Linux vorinstalliert ist:

   ```bash
   curl -v http://<ip-des-pico>/
   ```

   Mit `-v` sehen Sie die komplette Anfrage und Antwort, auch die Statuszeile und die Header.
2. **`GET /config` mit JSON.** Wert aus der geladenen Konfiguration nehmen, mit `json.dumps()` in einen String verwandeln, `Content-Type: application/json` setzen.
3. **`POST /config`.** Den JSON-Body aus der Anfrage lesen, mit `json.loads()` parsen, Werte übernehmen. Test:

   ```bash
   curl -v -X POST http://<ip-des-pico>/config \
        -H "Content-Type: application/json" \
        -d '{"reading_interval_seconds": 10}'
   ```

   Danach `GET /config` erneut aufrufen: Der neue Wert muss zurückkommen, und der Sensor muss ab jetzt im neuen Intervall senden.
4. **`GET /status`** nach dem Schema, das in der Gesamtgruppe vereinbart wurde.
5. **Falsche Anfragen.** Unbekannter Pfad, falsche Methode, kaputtes JSON: Der Server antwortet mit dem passenden Statuscode (404, 405, 400) und läuft weiter, statt abzustürzen.
6. **Testfälle** aus den `curl`-Aufrufen ableiten und im gewählten Werkzeug festhalten.

Sie können den Server mit `socketpool` selbst schreiben oder die Bibliothek [`adafruit_httpserver`](https://docs.circuitpython.org/projects/httpserver/en/latest/) aus dem Bundle verwenden, die Routen, JSON-Antworten und Statuscodes bereits kennt. Beides ist zulässig. Der eigene Server ist lehrreicher, die Bibliothek nimmt Ihnen die unten beschriebenen Stolpersteine ab. Auf dem ESP32 übernimmt das die Bibliothek `WebServer` aus dem Arduino-Core; die Reihenfolge der Schritte bleibt dieselbe.

### Hinweise zu den schwierigen Stellen

- **Die Hauptschleife darf nie blockieren.** Ihr Programm bedient MQTT, den Sensor und den Webserver in einer einzigen Schleife. Wartet ein Teil, stehen alle anderen. Zwei typische Bremsen: `accept()` wartet standardmäßig, bis ein Browser anklopft (Stichwort `setblocking(False)`), und `loop()` von MiniMQTT wartet standardmäßig bis zu einer Sekunde auf eingehende Nachrichten (Stichwort: Parameter `timeout`, und wie oft der Aufruf wirklich nötig ist, wenn Sie nichts abonniert haben).
- **Port 80 ist nach einem Neustart noch belegt.** Speichern Sie eine Datei, startet `code.py` neu, aber der alte Socket ist im WLAN-Modul noch nicht freigegeben. `bind()` schlägt dann mit `EADDRINUSE` fehl. Stichworte: `SO_REUSEADDR`, oder das Starten des Servers bei Fehler einige Sekunden später erneut versuchen, statt aufzugeben.
- **Die Anfrage kommt nicht in einem Stück.** Ein `recv()` liefert nicht zwingend die ganze Anfrage. Der Header `Content-Length` sagt Ihnen, wie viele Bytes Body Sie noch erwarten müssen. Der Body beginnt nach der ersten Leerzeile (`\r\n\r\n`).
- **Schreibschutz.** Standardmäßig darf CircuitPython nicht auf sein eigenes Laufwerk schreiben, damit der Laptop es über USB beschreiben kann. Das gilt auch, wenn der Pico nur an einer Powerbank hängt. Das Speichern der `settings.toml` aus `POST /config` scheitert dann mit einem `OSError`. Die Hinweise dazu stehen im Docstring von `ConfigManager.save_settings()` in der Vorlage. Für die Bewertung reicht es, wenn die neue Konfiguration im laufenden Betrieb übernommen wird und ein Fehler beim Speichern sauber gemeldet wird; das dauerhafte Speichern per `boot.py` ist ein Plus.
- **Test im Browser.** Ein Browser schickt bei jedem Aufruf zusätzlich `GET /favicon.ico`. Wenn Ihr Server darauf abstürzt, sehen Sie das nur in der seriellen Konsole.

### Was die IT-Abteilung wissen muss

Für den Absatz in der Dokumentation brauchen Sie die Fakten aus Ihrer eigenen Firmware. Notieren Sie, welche Verbindungen Ihr Gerät **ausgehend** aufbaut (Ziel, Port, Protokoll), z.B. zum Broker auf `158.180.44.197:1883` über TCP und, falls Sie NTP verwenden, zu einem Zeitserver über UDP 123. Notieren Sie außerdem, welche Verbindungen **eingehend** nötig sind (die HTTP-API auf Port 80, nur aus dem lokalen Netz). Daraus ergibt sich, was in der Whitelist stehen muss. Mit dem [Filius-Skript](https://jhumci.github.io/2024_SoSe_IoT1/IoT_5_Netzwerke_Aufgaben/) können Sie eine solche Firewall im Simulator nachbauen.

::: {.callout-warning collapse="true"}
## Typische Probleme
- **`curl: (7) Connection refused`**: Der Server läuft nicht, z.B. weil `bind()` fehlgeschlagen ist. Serielle Konsole prüfen.
- **`curl` hängt und läuft in einen Timeout**: Der Server nimmt die Verbindung an, antwortet aber nicht. Meist blockiert etwas in der Hauptschleife, oder die Antwort wird gesendet, bevor die Anfrage vollständig gelesen wurde.
- **Antwort dauert über eine Sekunde**: Siehe *Die Hauptschleife darf nie blockieren*.
- **Erste Anfrage geht, zweite nicht**: Die Client-Verbindung wird nach der Antwort nicht geschlossen, oder eine Exception im Handler beendet die Schleife.
- **Laptop findet den Pico nicht**: Anderes WLAN, oder das WLAN trennt Clients voneinander (Gäste-Netz, Client-Isolation). Ein Handy-Hotspot ist die einfachste Umgebung zum Testen.
:::

# Asynchrone Inhalte

Mit folgenden Inhalten sollten Sie sich vertraut machen, um die Aufgabenstellung erfolgreich zu bearbeiten:

- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status): Eine Übersicht über die verschiedenen HTTP-Statuscodes und deren Bedeutung.
- [Aufbau einer HTTP-Nachricht](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages): Statuszeile, Header, Leerzeile, Body. Genau das muss Ihr Server lesen und schreiben.
- [Everything curl](https://everything.curl.dev/): Nachschlagewerk für `curl`. Für den Einstieg reichen die Kapitel zu `-v`, `-X` und `-d`.
- [RESTful API Resource Naming](https://restfulapi.net/resource-naming/): Empfehlungen zur Benennung von Ressourcen in RESTful APIs.
- [OpenAPI Specification](https://learn.openapis.org/): Einführung in das Format von `openapi.yaml`. Mit dem [Swagger Editor](https://editor.swagger.io/) können Sie die Datei prüfen und lesbar darstellen.
- [`socketpool` in CircuitPython](https://docs.circuitpython.org/en/latest/shared-bindings/socketpool/index.html): Die Socket-API des Pico W, falls Sie den Server selbst schreiben.
- [`adafruit_httpserver`](https://docs.circuitpython.org/projects/httpserver/en/latest/): Die Alternative dazu, mit Beispielen für JSON-Antworten.
- [Filius-Aufgaben](https://jhumci.github.io/2024_SoSe_IoT1/IoT_5_Netzwerke_Aufgaben/): Ein Netzwerk-Simulator, der es ermöglicht, Netzwerktopologien zu erstellen und zu testen. Nutzen Sie das Skript und bearbeiten Sie die Aufgaben 1-12, 21, 22 im Skriptum, um sich mit den Grundlagen von Netzwerken vertraut zu machen.

---

# Datei: `docs/Termin_3_Cloud.qmd`

# Synchron

## [Cloud Computing und Virtualisierung](https://jhumci.github.io/2023_WiSe_IoT2/IoT_7_Cloud/#)

## [Security und Safety](https://jhumci.github.io/2023_WiSe_IoT2/IoT_6_SecuritySafety/)

## Vorstellung der Aufgabenstellung

Sie bereiten eine containerisierte Lösung vor, die eine Datenhaltung (z.B. InfluxDB, SQLite, DuckDB, CSV) und eine Visualisierungskomponente (z.B. Grafana) beinhaltet. Bei der Auswahl der Technologien sind Sie frei, achten Sie jedoch darauf, dass die Lösung ressourcenschonend ist und auf einem typischen Laptop ausgeführt werden kann.

### Voraussetzungen (für jede Bewertungsstufe)

- [ ] Die Lösung lässt sich mit minimalem Aufwand starten, z.B. mit `docker compose up` über eine `docker-compose.yml`.
- [ ] Die Dokumentation ist so aufbereitet, dass ein Nutzer den Mikrocontroller über die Konfiguration in ein bestehendes WLAN einbinden sowie die containerisierte Lösung starten und nutzen kann.

### Bewertungsstufen

Die Stufen bauen aufeinander auf:

| Bewertung | Anforderung |
|---|---|
| *genügend* | Die Live-Daten Ihres Sensors werden vom MQTT-Broker gelesen, gespeichert (eine CSV-Datei reicht) und visualisiert. |
| *befriedigend* | Die Daten werden in einer echten Datenbank gespeichert (z.B. InfluxDB, SQLite, DuckDB) statt in einer CSV-Datei. |
| *gut* | Neue Sensoren werden ohne zusätzlichen Konfigurationsaufwand automatisch aufgenommen, z.B. die Daten aller Gruppen über das Topic `iiot/group/+/sensor/temperature/state`. |
| *sehr gut* | Neben den Zeitreihen bietet die Lösung eine Übersicht über die verbundenen Sensoren (z.B. Anzahl der Sensoren, letzte Verbindung, Status aus dem Topic `iiot/group/+/status`). |

**Bonus:** Zusätzliche Kennzahlen wie Mittelwert, Minimum und Maximum werden positiv berücksichtigt und können Schwächen in anderen Bereichen ausgleichen.

::: {.callout-note}
Die Bewertungsstufen beziehen sich auf den Implementierungsumfang. Codequalität, Integration der Komponenten und Dokumentation fließen wie in den [Bewertungskriterien](../index.qmd#bewertungskriterien) beschrieben zusätzlich in die Bewertung ein.
:::

### Einstieg

Bevor Sie Container bauen, prüfen Sie, dass Sie die Daten überhaupt sehen. Der schnellste Weg ist ein Abonnement auf alle Sensor-Topics, mit denselben Zugangsdaten, die auch Ihr Gerät verwendet:

```bash
mosquitto_sub -h 158.180.44.197 -p 1883 -u bobm -P '<passwort>' -t 'iiot/group/+/sensor/#' -v
```

`mosquitto_sub` gehört zum [Mosquitto](https://mosquitto.org/download/)-Paket. Dasselbe erreichen Sie mit rund zehn Zeilen Python und der Bibliothek [`paho-mqtt`](https://pypi.org/project/paho-mqtt/). Dieses Skript ist zugleich der Kern Ihres ersten Containers: Es empfängt die Nachrichten und schreibt sie weg, zunächst in eine CSV-Datei. Die Datenbank und die Visualisierung kommen danach.

# Asynchrone Inhalte

Mit folgenden Inhalten sollten Sie sich vertraut machen, um die Aufgabenstellung erfolgreich zu bearbeiten:

- [DuckDB](https://duckdb.org/): Leichtgewichtige Datenbank für Zeitreihendaten
- [InfluxDB](https://www.influxdata.com/products/influxdb-overview/): Zeitseriendatenbank
    - [telegraf](https://www.influxdata.com/time-series-platform/telegraf/): Vermittlung zwischen MQTT und InfluxDB
    - [Grafana](https://grafana.com/): Visualisierung von Zeitseriendaten
- [Apache NiFi](https://nifi.apache.org/): Apache NiFi
- [node-red](https://nodered.org/): Low-Code-Entwicklungsumgebung für die Vernetzung von IoT-Geräten
- [Docker](https://www.docker.com/): Containerisierungstechnologie

---

# Datei: `docs/iot-specs/asyncapi.yaml`

```yaml
asyncapi: 2.6.0
info:
  title: Building IoT Sensors
  version: '1.1.0'
  description: |
    AsyncAPI-Spezifikation für Gebäudesensoren.
    Dieses Beispiel zeigt einen Temperatur-Sensor in einem Raum.

defaultContentType: application/json

servers:
  mqttBroker:
    url: 158.180.44.197:1883
    protocol: mqtt
    protocolVersion: '5'
    description: Privater Kurs-Broker (unverschlüsselt, Zugangsdaten siehe conventions.md)

channels:
  iiot/group/{group}/sensor/temperature/state:
    description: |
      Publiziert Temperaturmessungen einer Gruppe
    parameters:
      group:
        $ref: '#/components/parameters/group'
    publish:
      operationId: publishTemperature
      summary: Sendet Temperaturdaten
      message:
        messageId: temperatureMessage
        name: TemperatureMessage
        title: Temperatur-Daten
        payload:
          $ref: '#/components/schemas/TemperatureReading'

  iiot/group/{group}/status:
    description: |
      Status des Geräts einer Gruppe. Nach dem Verbindungsaufbau wird "ok" gesendet,
      bei Fehlern (z.B. ungültige Sensordaten) "error". Als Last Will and Testament
      wird "offline" hinterlegt, das der Broker bei unerwartetem Verbindungsabbruch sendet.
      Nachrichten werden retained gesendet, damit neue Subscriber den letzten Status sehen.
    parameters:
      group:
        $ref: '#/components/parameters/group'
    publish:
      operationId: publishStatus
      summary: Sendet den Gerätestatus
      bindings:
        mqtt:
          qos: 1
          retain: true
      message:
        messageId: statusMessage
        name: StatusMessage
        title: Geräte-Status
        payload:
          $ref: '#/components/schemas/DeviceStatus'

components:
  parameters:
    group:
      description: |
        Nachnamen aller Gruppenmitglieder in Kleinbuchstaben, mit "-" getrennt
        (nachname1-nachname2-nachname3), z.B. "mustermann-meier-schmidt"
      schema:
        type: string

  schemas:
    Status:
      type: string
      description: Statuswerte laut conventions.md
      enum: [ok, error, offline]
      example: "ok"

    TemperatureReading:
      type: object
      required:
        - timestamp
        - value
        - unit
      properties:
        timestamp:
          type: string
          format: date-time
          description: Zeitpunkt der Messung (ISO8601)
          example: "2025-08-28T10:00:00Z"
        sensor_id:
          type: string
          description: Eindeutige ID des Sensors aus der Konfiguration
          example: "temp-101"
        value:
          type: number
          description: Gemessene Temperatur
          example: 22.5
        unit:
          type: string
          description: Einheit der Messung
          enum: [°C, K]
          example: "°C"
        status:
          $ref: '#/components/schemas/Status'

    DeviceStatus:
      type: object
      required:
        - status
      properties:
        status:
          $ref: '#/components/schemas/Status'
        timestamp:
          type: string
          format: date-time
          description: |
            Zeitpunkt der Statusmeldung (ISO8601). Optional, da die "offline"-Nachricht
            (Last Will) bereits beim Verbindungsaufbau festgelegt wird.
          example: "2025-08-28T10:00:00Z"
        sensor_id:
          type: string
          description: Eindeutige ID des Sensors aus der Konfiguration
          example: "temp-101"
```

---

# Datei: `docs/iot-specs/conventions.md`

# MQTT & Daten-Konventionen

## Topics
- Struktur: `iiot/group/{nachname1-nachname2-nachname3}/sensor/temperature/state`
- Nur Kleinbuchstaben und `/` als Trenner
- Beispiel: `iiot/group/mustermann-meier-schmidt/sensor/temperature/state`
- Gerätestatus: `iiot/group/{nachname1-nachname2-nachname3}/status` (retained, Last Will = `offline`)

## Payload
- Standardformat: JSON
- Zeitstempel immer in **UTC, ISO8601** (`2025-08-28T10:00:00Z`)
- Einheit als String (z. B. `"°C"`)
- Statuswerte: `ok`, `error`, `offline`

## Endpunkt

- Host: `158.180.44.197` (privater Kurs-Broker)
- Port: 1883
- Username: `bobm`
- Password: In Vorlesung erfragen
- SSL/TLS: False
- Client-ID: Nach eigener Konfiguration
- MQTT-Version: 5.0

# REST-API Konventionen

- Endpunkte sind **unverschlüsselt (HTTP)** erreichbar.
- Standard-Port: `80`
- Basis-URL: `http://<deviceIp>/`

## Endpunkte
### `/config`
- **GET**: Gibt aktuelle Konfiguration zurück.
- **POST**: Setzt neue Konfiguration.

### Beispiel `GET /config` Response
Die Feldnamen entsprechen den Schlüsseln in `settings.toml`.
```json
{
  "device_id": "yourmuesli-innsbruck-01",
  "reading_interval_seconds": 60
}
```

Weitere Felder sowie der Endpunkt `/status` werden in der Gesamtgruppe festgelegt
und in `openapi.yaml` ergänzt.

---

# Datei: `docs/iot-specs/openapi.yaml`

```yaml
openapi: 3.0.3
info:
  title: MECH-M-3-IIoT ESP32 REST API
  description: Unverschlüsselte lokale HTTP-Schnittstelle zur Konfiguration und Diagnose.
  version: 2.0.0
servers:
  - url: http://{deviceIp}
    variables:
      deviceIp: {default: 192.168.0.100}
paths:
  /:
    get:
      operationId: getRoot
      summary: Erreichbarkeit prüfen
      responses:
        '200':
          description: Gerät ist erreichbar
          content:
            text/plain:
              schema: {type: string}
    post:
      responses:
        '405': {$ref: '#/components/responses/MethodNotAllowed'}
  /config:
    get:
      operationId: getConfig
      summary: Aktuelle Konfiguration abrufen
      responses:
        '200':
          description: Aktuelle Konfiguration
          content:
            application/json:
              schema: {$ref: '#/components/schemas/Config'}
    post:
      operationId: updateConfig
      summary: Sendeintervall im laufenden Betrieb ändern
      requestBody:
        required: true
        content:
          application/json:
            schema: {$ref: '#/components/schemas/ConfigUpdate'}
      responses:
        '200':
          description: Konfiguration übernommen
          content:
            application/json:
              schema: {$ref: '#/components/schemas/UpdateResult'}
        '400': {$ref: '#/components/responses/BadRequest'}
    put:
      responses:
        '405': {$ref: '#/components/responses/MethodNotAllowed'}
  /status:
    get:
      operationId: getStatus
      summary: Laufzeit-, Verbindungs- und Messstatus abrufen
      responses:
        '200':
          description: Aktueller Gerätestatus
          content:
            application/json:
              schema: {$ref: '#/components/schemas/DeviceStatus'}
    post:
      responses:
        '405': {$ref: '#/components/responses/MethodNotAllowed'}
components:
  responses:
    BadRequest:
      description: Ungültiges JSON oder ungültiger Wert
      content:
        application/json:
          schema: {$ref: '#/components/schemas/Error'}
    MethodNotAllowed:
      description: HTTP-Methode ist für diesen Pfad nicht erlaubt
      headers:
        Allow:
          schema: {type: string}
      content:
        application/json:
          schema: {$ref: '#/components/schemas/Error'}
  schemas:
    Config:
      type: object
      required: [device_id, reading_interval_seconds, location]
      properties:
        device_id: {type: string, example: yourmuesli-innsbruck-01}
        reading_interval_seconds: {type: integer, minimum: 2, maximum: 86400, example: 60}
        location: {type: string, example: 'Produktionshalle 1, Innsbruck'}
    ConfigUpdate:
      type: object
      required: [reading_interval_seconds]
      additionalProperties: false
      properties:
        reading_interval_seconds: {type: integer, minimum: 2, maximum: 86400}
    UpdateResult:
      type: object
      required: [status]
      properties:
        status: {type: string, enum: [updated]}
    DeviceStatus:
      type: object
      required: [device_id, wifi_connected, mqtt_connected, clock_synchronized, ip, uptime_seconds, last_publish_successful, last_readings]
      properties:
        device_id: {type: string}
        wifi_connected: {type: boolean}
        mqtt_connected: {type: boolean}
        clock_synchronized: {type: boolean}
        ip: {type: string}
        uptime_seconds: {type: integer, minimum: 0}
        last_publish_successful: {type: boolean}
        seconds_since_last_publish: {type: integer, nullable: true, minimum: 0}
        last_readings:
          type: object
          properties:
            temperature_c: {type: number}
            humidity_percent: {type: number, minimum: 0, maximum: 100}
            hygrometer_1_percent: {type: number, minimum: 0, maximum: 100}
            hygrometer_2_percent: {type: number, minimum: 0, maximum: 100}
    Error:
      type: object
      required: [error]
      properties:
        error: {type: string}
```

---

# Datei: `index.qmd`

# Einleitung

Herzlich willkommen zur Lehrveranstaltung __Industrial Internet of Things__! Die folgenden Unterlagen beziehen sich auf die ersten drei synchronen Termine der Vorlesung, welche von Christoph Egger durchgeführt und bewertet werden.

Im Rahmen dieser Abgabe erweitern Sie Ihr Verständnis für die Kernkonzepte des Industrial IoT, insbesondere die Erfassung, Übertragung, Speicherung und Analyse von Sensordaten in Echtzeit sowie den Umgang mit Konfigurationsdaten.

Im ersten Teil der Vorlesung von Christoph Egger, werden wir Grundkonzepte und Technologien des IIoT behandeln und mit einem Mikrocontroller (z.B. Raspberry Pi Pico W) kennenlernen. Im zweiten Teil der Vorlesung von Thomas Konecny, werden die Themen aufgegriffen und mit modernen Operational-Technologien (Beckhoff SPS, AWS-Cloud) vertieft.

::: {.callout-note}
## Feedback
Feedback und Anregungen sind jederzeit willkommen – gerne mündlich oder direkt über das GitHub Repository.
:::

## Zusammenarbeit
Die Kommunikation findet über das gemeinsam genutzte [Repository](https://github.com/jhumci/MECH-M-3-IIoT) statt. Im Wiki sind alle relevanten Informationen zu Hintergrund, Aufgabenstellung und Anforderungen zu finden.
Für die asynchrone Kommunikation mit der Lehrveranstaltungsleitung sollen *Issues* und *Pull Requests* im GitHub Repository genutzt werden. Die Abgabe erfolgt über den Link zu einem Fork des Original-Repositories, spätestens am **Freitag, 27.11.2026, 23:59 Uhr**.

## Einsatz von Generativer KI
Es wird davon ausgegangen, dass sowohl in der Wissensermittlung als auch in der Umsetzung generative KI-Tools (z.B. ChatGPT, GitHub Copilot) eingesetzt werden. Dies ist ausdrücklich erlaubt und wird nicht negativ bewertet.

Wichtig ist hierbei, dass Sie **reflektiert** damit umgehen:

### Bei der Wissensermittlung

- Kontext ist entscheidend. Formulieren Sie Ihre Fragen so, dass Sie eine Antwort erhalten, die auf Ihr konkretes Problem zugeschnitten ist. Füllen Sie die vorhandenen Input-Token mit Aufgabenbeschreibung, Anforderungen, Rahmenbedingungen, Dokumentationen, Code-Snippets, Fehlermeldungen, etc.
- Fragen sie nicht nach der Lösung, sondern nach Lösungsoptionen. Lassen Sie sich verschiedene Ansätze und deren Vor- und Nachteile aufzeigen.

### Bei der Umsetzung

- Berücksichtigen Sie, dass ein großer Teil der Trainingsdaten von generativer KI oft einfache Beispiele und keine Teile von komplexen Systemen sind. Wenn Sie nach einer Lösung fragen, werden Sie oft bei einfachen Lösungen landen, die nicht mit ihrem Projekt mitwachsen können.
- Berücksichtigen Sie, dass es verschiedene Werkzeuge für verschiedene Aufgaben gibt. Nutzen Sie die Stärken der Werkzeuge, aber seien Sie sich auch der Schwächen bewusst. Die **Autovervollständigung von Code** ist oft hilfreich, schafft es aber nicht immer den gesamten Kontext der Systemarchitektur zu verstehen. Nutzen Sie z.B. stattdessen **ChatGPT** um sich einen Vorschlag für eine Systemarchitektur geben zu lassen und die von ihm erzeugten Ordner und Dateien erklären zu lassen. Für die Softwareentwicklung gibt es auch Tools, wie **GitHub Copilot im Agent Mode** oder **Gemini CLI**, die zugriff auf das gesamte Repository und ihre Shell haben.


## Bewertungskriterien

Die Arbeit erfolgt in Gruppen, die im ersten Termin eingeteilt werden. Die Gruppengröße richtet sich nach der verfügbaren Hardware. Das sich inhaltlich und qualitativ an den Anforderungen orientierende Gesamtkonzept wird bewertet. Dabei werden folgende Kriterien berücksichtigt:

- Nutzerfreundlichkeit und Dokumentation:
    - Wie einfach ist es für einen neuen Nutzer, das System einzurichten und zu verwenden?
    - Wie gut ist die Dokumentation? (Klarheit, Vollständigkeit, Struktur)
    - Funktionieren die bereitgestellten Testfälle?
- Implementierungsqualität:
    - Wie gut ist die Qualität des Codes? (Lesbarkeit, Wartbarkeit, Modularität)
    - Wie gut sind die Implementierung der REST-Schnittstelle und die Nutzung der OpenAPI Specification?
    - Wie gut ist die Integration der verschiedenen Komponenten (Firmware, Datenbank, Analyse)
- Implementierungsumfang:
    - Wie gut erfüllt die Lösung die gestellten Anforderungen?
    - Bei einigen Anforderungen gibt es Abstufungen, die in der Aufgabenstellung beschrieben sind. 

::: {.callout-important}
## Bewertung
Die Bewertung der beiden Teile von IIoT erfolgt unabhängig voneinander. Die Noten (MCI-Punkte) werden anhand der SWS-Verteilung gemittelt. Zum Bestehen sind insgesamt 60% erforderlich.
:::


## Storyline
Sie sind Teil eines Teams, das eine IoT-Lösung für die Überwachung von Umgebungsbedingungen in einer Produktionsanlage entwickelt. Ihre Aufgabe ist es, eine Lösung zu entwerfen und zu implementieren, die Sensordaten erfasst, diese sicher überträgt und in Echtzeit analysiert, um Anomalien zu erkennen und Berichte zu generieren.

<iframe width="800" height="320" src="https://www.youtube.com/embed/e9Jyv7h8mo0" title="MCI | Teaching Factory | Side by side" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Der Frühstücksflockenhersteller yourmuesli.at stellt an vielen Produktionsstandorten Müsli-Mischungen her. Der Abfüllprozess wird stark durch Umweltparameter, wie Temperatur und Luftfeuchtigkeit beeinflusst. Um die Qualität der Produkte sicherzustellen, ist eine kontinuierliche Überwachung dieser Parameter erforderlich. Bisher wurde dies stark vernachlässigt. Zunehmende Probleme, wie nicht mehr knusprige Cornflakes, geschmolzene Schokolade und andere Qualitätsmängel, sind aufgetreten. Es braucht keine Natural Language Processing und keine Sentiment-Analyse um die negativen Kundenbewertungen zu erkennen:

> „@yourmuesli_at, sogts amoi: Solln die Haferflockn im Müsli wirklich so latschert sein wia a Regentog in Innsbruck? 🤨 Und die Schoko pickt zsamm wia a Lawinabrettl. So schmeckt des nit, gell! #MüsliFail“

> „@yourmuesli_at, des Früchtemüsli schmeckt so trocken, i brauch mehr Milch als a ganzes Kalb. 🐄 So kaunst koan Tiroler ned füttern!“

> „@yourmuesli_at, die Portion is so kloan, do werd in Tirol grad amol a Spatzl satt. Mia brauchn a gscheids Müsli, nit a Vogelfutter!“

Das Management hat beschlossen, dass eine schnelle Reaktion erforderlich ist. Bis zum __27.11.2026__ möchte der Leiter der Qualitätssicherung Bruno Mircevski die Temperaturwerte aller Produktionsstandorts weltweit auf einem Dashboard auf seinem iPhone sehen.

Da die [_Beckhoff EL3204_](https://www.beckhoff.com/de-at/produkte/i-o/ethercat-klemmen/el3xxx-analog-eingang/el3204.html) zur Zeit eine Lieferzeit von wenigen Wochen haben, kommt es nicht in Frage die bestehende Hardware zu erweitern. Sie und Ihr Team müssen daher eine alternative Lösung entwickeln, welche schnell umsetzbar, kostengünstig und vor allem einfach weltweit zu implementieren und zu warten ist. Das bedeutet, dass sie die Lösungen zentral von Innsbruck aus entwickeln und die Hardware versenden können. Vor Ort, soll die Hardware möglichst einfach an die Produktionsanlagen angeschlossen und ggf. konfiguriert werden können. Das soll anhand einer einfachen Doku auch für technisch nicht sehr versierte Nutzer:innen möglich sein. Zudem sollen Sie auch auf die Ferne dazu in der Lage sein, den Zustand der Sensoren zu überwachen und wenn nötig Einstellungen zu ändern.

::: {.callout collapse="true"}
# Aufgabenstellung
Die Problemlösung wird in drei Teile unterteilt, welche jeweils mit einer kurzen synchronen Einheit beginnen. In dieser wird eine kurze Einführung in das Thema gegeben und der nächste Teil der Aufgabenstellung vorgestellt. Für die asynchronen Einheiten wird Ihnen weiteres Material zum Einarbeiten und Vorbereiten der Aufgabenstellung zur Verfügung gestellt.

## Termin 1: Grundkonzepte
Eine kostengünstige Lösung zur Erfassung und Übertragung der Sensordaten wäre z.B. der Einsatz von Microcontroller-Plattformen wie dem Raspberry Pi Pico W oder ESP32, die vor Ort in ein WLan integriert werden können. Hierzu kommen z.B. der Raspberry Pi Pico W mit CircuitPython (Vorlage in diesem Repository) oder der ESP32 mit Arduino in Frage. Als Sensor wird der DHT11 (Temperatur und Luftfeuchtigkeit) eingesetzt. Da es schnell gehen soll, wird auf ein eigenes Printed Circuit Board Design verzichtet. Zur Datenübertragung kommen auf Anwendungsschicht z.B. MQTT, HTTP oder FTP in Frage.

## Termin 2: Netzwerke
Da Informationen weltweit ausgetauscht werden müssen, ist der Einsatz von TCP/IP-Protokollen unerlässlich. Sie müssen sich Gedanken machen, wie die Netzwerkeinstellungen konfiguriert werden, um eine zuverlässige Kommunikation zwischen den Geräten zu gewährleisten. Zudem werden Sie der IT-Abteilung vor Ort ggf. Anweisungen geben müssen, wie die Firewalls angepasst werden müssen.
Die Firmware der Microcontroller soll zudem eine HTTP-Schnittstelle zur Konfiguration bereitstellen, über den z.B. das Sende-Intervall angepasst werden kann, so dass Sie diese aus der Ferne warten können. Dies ist aber nur möglich, wenn sie sich im gleichen Netzwerk, wie die Mikrocontroller befinden.

## Termin 3: Cloud
Da noch nicht klar ist, wo das Dashboard in Zukunft laufen soll, entwickeln Sie direkt in einem Container. Sie bereiten einen oder mehrere Container vor, in welchen die Datenhaltung und Auswertung erfolgen. Anforderung hier ist, dass ein Container gestartet werden kann, der sowohl die Daten aller verbundener Sensoren speichert als auch die eigenen Daten visualisiert.
:::

---

# Datei: `pyproject.toml`

```toml
[project]
name = "MECH-M-3-IIoT"
version = "0.1.0"
description = "Industrial Internet of Things (MECH-M-DUAL-3-IOT): Aufgabenstellung, Spezifikationen und Vorlagen"
authors = [
    {name = "jhumci", email = "julian.huber@mci.edu"},
    {name = "Christoph Egger"},
]
dependencies = ["quarto-cli>=1.5"]
requires-python = "==3.12.*"
readme = "README.md"
license = {text = "MIT"}


[tool.pdm]
distribution = false
```

---

# Datei: `src/cloud/Dockerfile`

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

RUN mkdir -p /data && chown -R 65532:65532 /data /app
USER 65532:65532

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "app:app"]
```

---

# Datei: `src/cloud/app.py`

```python
import json
import logging
import os
import sqlite3
import threading
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request
import paho.mqtt.client as mqtt

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
LOG = logging.getLogger("iiot-dashboard")

DATABASE = Path(os.getenv("DATABASE_PATH", "/data/iiot.sqlite3"))
MQTT_HOST = os.getenv("MQTT_HOST", "158.180.44.197")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "bobm")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TLS = os.getenv("MQTT_TLS", "false").lower() in {"1", "true", "yes"}

app = Flask(__name__)
db_lock = threading.Lock()


def connect_db():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with db_lock, closing(connect_db()) as db:
        db.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL,
                sensor_type TEXT NOT NULL,
                sensor_id TEXT,
                measured_at TEXT NOT NULL,
                received_at TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                status TEXT NOT NULL,
                topic TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_readings_lookup
                ON readings(group_name, sensor_type, measured_at);
            CREATE TABLE IF NOT EXISTS device_status (
                group_name TEXT PRIMARY KEY,
                sensor_id TEXT,
                status TEXT NOT NULL,
                measured_at TEXT,
                received_at TEXT NOT NULL,
                topic TEXT NOT NULL
            );
            """
        )
        db.commit()


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_topic(topic):
    parts = topic.split("/")
    if len(parts) == 4 and parts[:2] == ["iiot", "group"] and parts[3] == "status":
        return parts[2], "status"
    if len(parts) == 6 and parts[:2] == ["iiot", "group"] and parts[3] == "sensor" and parts[5] == "state":
        return parts[2], parts[4]
    return None, None


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code != 0:
        LOG.error("MQTT connection failed: %s", reason_code)
        return
    LOG.info("Connected to MQTT broker %s:%s", MQTT_HOST, MQTT_PORT)
    client.subscribe("iiot/group/+/sensor/+/state", qos=1)
    client.subscribe("iiot/group/+/status", qos=1)


def on_message(client, userdata, message):
    group_name, message_type = parse_topic(message.topic)
    if not group_name:
        return
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        received_at = utc_now()
        with db_lock, closing(connect_db()) as db:
            if message_type == "status":
                status = str(payload["status"])
                if status not in {"ok", "error", "offline"}:
                    raise ValueError("invalid status")
                db.execute(
                    """INSERT INTO device_status
                       (group_name, sensor_id, status, measured_at, received_at, topic)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ON CONFLICT(group_name) DO UPDATE SET
                         sensor_id=excluded.sensor_id, status=excluded.status,
                         measured_at=excluded.measured_at, received_at=excluded.received_at,
                         topic=excluded.topic""",
                    (group_name, payload.get("sensor_id"), status,
                     payload.get("timestamp"), received_at, message.topic),
                )
            else:
                value = float(payload["value"])
                measured_at = str(payload["timestamp"])
                unit = str(payload["unit"])
                status = str(payload.get("status", "ok"))
                db.execute(
                    """INSERT INTO readings
                       (group_name, sensor_type, sensor_id, measured_at, received_at,
                        value, unit, status, topic)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (group_name, message_type, payload.get("sensor_id"), measured_at,
                     received_at, value, unit, status, message.topic),
                )
            db.commit()
    except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as error:
        LOG.warning("Rejected message on %s: %s", message.topic, error)


def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="iiot-group1-dashboard")
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    if MQTT_TLS:
        client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()
    return client


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/sensors")
def sensors():
    with closing(connect_db()) as db:
        rows = db.execute(
            """SELECT r.group_name, r.sensor_type, r.sensor_id,
                      COUNT(*) AS samples, MIN(r.value) AS minimum,
                      MAX(r.value) AS maximum, AVG(r.value) AS average,
                      MAX(r.measured_at) AS last_measurement,
                      s.status AS device_status, s.received_at AS last_status_received
               FROM readings r
               LEFT JOIN device_status s ON s.group_name = r.group_name
               GROUP BY r.group_name, r.sensor_type, r.sensor_id
               ORDER BY r.group_name, r.sensor_type"""
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.get("/api/readings")
def readings():
    group_name = request.args.get("group")
    sensor_type = request.args.get("sensor", "temperature")
    limit = min(max(request.args.get("limit", 200, type=int), 1), 2000)
    query = "SELECT * FROM readings WHERE sensor_type = ?"
    parameters = [sensor_type]
    if group_name:
        query += " AND group_name = ?"
        parameters.append(group_name)
    query += " ORDER BY measured_at DESC LIMIT ?"
    parameters.append(limit)
    with closing(connect_db()) as db:
        rows = db.execute(query, parameters).fetchall()
    return jsonify([dict(row) for row in reversed(rows)])


DASHBOARD = """
<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IIoT Sensor Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
body{font-family:system-ui;margin:0;background:#0f172a;color:#e2e8f0}main{max-width:1200px;margin:auto;padding:24px}
h1{margin-bottom:4px}.muted{color:#94a3b8}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:22px 0}
.card,.chart{background:#1e293b;border-radius:12px;padding:16px}.ok{color:#4ade80}.error,.offline{color:#fb7185}
select{background:#334155;color:white;padding:8px;border:0;border-radius:6px}canvas{max-height:430px}
</style></head><body><main><h1>IIoT Sensor Dashboard</h1><p class="muted">Live-Daten aller Gruppen · automatische Aktualisierung</p>
<label>Gruppe: <select id="group"></select></label><section class="cards" id="cards"></section>
<section class="chart"><canvas id="chart"></canvas></section></main>
<script>
let chart; async function refresh(){const sensors=await fetch('/api/sensors').then(r=>r.json());
const groups=[...new Set(sensors.map(s=>s.group_name))];const select=document.querySelector('#group');
const previous=select.value;if(select.options.length!==groups.length){select.innerHTML=groups.map(g=>`<option>${g}</option>`).join('');if(groups.includes(previous))select.value=previous;}
const group=select.value||groups[0];const rows=sensors.filter(s=>s.group_name===group);
document.querySelector('#cards').innerHTML=rows.map(s=>`<article class="card"><strong>${s.sensor_type}</strong><p>Status: <span class="${s.device_status}">${s.device_status||'unbekannt'}</span></p><p>${s.samples} Werte</p><small>Min ${fmt(s.minimum)} · Ø ${fmt(s.average)} · Max ${fmt(s.maximum)}</small></article>`).join('');
if(!group)return;const data=await fetch(`/api/readings?group=${encodeURIComponent(group)}&sensor=temperature`).then(r=>r.json());
const config={type:'line',data:{labels:data.map(x=>x.measured_at),datasets:[{label:'Temperatur °C',data:data.map(x=>x.value),borderColor:'#38bdf8',tension:.2}]},options:{responsive:true,scales:{x:{ticks:{color:'#94a3b8'}},y:{ticks:{color:'#94a3b8'}}}}};
if(chart)chart.destroy();chart=new Chart(document.querySelector('#chart'),config)}function fmt(v){return v==null?'–':Number(v).toFixed(2)}
document.querySelector('#group').addEventListener('change',refresh);refresh();setInterval(refresh,10000);
</script></body></html>
"""


@app.get("/")
def dashboard():
    return render_template_string(DASHBOARD)


initialize_database()
mqtt_client = None if os.getenv("DISABLE_MQTT") == "1" else start_mqtt()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

---

# Datei: `src/cloud/requirements.txt`

```text
Flask==3.1.2
gunicorn==23.0.0
paho-mqtt==2.1.0
```

---

# Datei: `src/esp32_firmware/.env.example`

```dotenv
# Anmeldedaten für das Projekt
# Kopieren Sie diese Datei nach .env und tragen Sie Ihre Daten ein.
# Die Datei .env wird NICHT ins Repository eingecheckt (.gitignore).

# Schalter: jeweils "zentrum" oder "kurs" bzw. "emqx" oder "kurs".
WIFI_PROFILE="zentrum"
MQTT_PROFILE="kurs"

# WLAN-Profil "zentrum"
WIFI_SSID="ZentrumPRA-2"
WIFI_PASSWORD="WLAN_PASSWORT_EINTRAGEN"

# WLAN-Profil "kurs"
KURS_SSID="KURS_WLAN_SSID_EINTRAGEN"
KURS_PASSWORD="KURS_WLAN_PASSWORT_EINTRAGEN"

# Broker-Profil "emqx"
MQTT_HOST="e2f0071d.ala.eu-central-1.emqxsl.com"
MQTT_USER="IIoT"
MQTT_PASSWORD="EMQX_PASSWORT_EINTRAGEN"
MQTT_USE_TLS="true"

# Broker-Profil "kurs": Host 158.180.44.197, Port 1883, Benutzer bobm und
# TLS=false werden automatisch gesetzt. Nur das Passwort wird benötigt.
MQTT_KURS_BROKER_PASS="IN_DER_VORLESUNG_ERFRAGEN"
```

---

# Datei: `src/esp32_firmware/.gitignore`

```gitignore
.pio
.vscode/.browse.c_cpp.db*
.vscode/c_cpp_properties.json
.vscode/launch.json
.vscode/ipch
.env
```

---

# Datei: `src/esp32_firmware/README.md`

# IIoT-Sensor – ESP32-C3, DHT20 und Hygrometer

Die Firmware setzt die Vorgaben aus `MECH-M-3-IIoT` um und verwendet die
Hardware aus diesem Projekt: einen DHT20 über I²C sowie zwei analoge
Hygrometer-Sensoren.

> Das MQTT-Passwort des Kurs-Brokers wird in der Vorlesung bekanntgegeben.
> Vor dem Upload müssen WLAN und MQTT-Zugangsdaten in `.env` eingetragen
> werden. Diese lokale Datei wird nicht committed.

## Hardware-Konfiguration

| Komponente | ESP32-C3-Pin | Funktion |
|---|---:|---|
| DHT20 SDA | GPIO 8 | I²C-Datenleitung |
| DHT20 SCL | GPIO 9 | I²C-Taktleitung |
| Hygrometer 1 Signal | GPIO 0 / A0 | Analogeingang, 0–3 V |
| Hygrometer 2 Signal | GPIO 1 | Analogeingang, 0–3 V |
| Sensor-Versorgung | 3.3 V | Versorgung |
| Sensor-Masse | GND | Masse |

## WLAN und Upload

1. PlatformIO und die Espressif32-Plattform in VS Code installieren.
2. `.env.example` nach `.env` kopieren und die Zugangsdaten eintragen.
3. Prüfen, dass der Gruppen-Slug `unterhuber-brachmann-reimeir-noessing` lautet.
4. ESP32-C3 über USB anschließen.
5. Mit `pio run -t upload` flashen.
6. Die serielle Ausgabe mit `pio device monitor --baud 115200` öffnen.

Die lokale `.env` ist in `.gitignore` ausgeschlossen und enthält das WLAN- sowie
das MQTT-Passwort.

## Profilumschaltung

WLAN und Broker werden unabhängig über zwei Werte in `.env` ausgewählt:

```text
WIFI_PROFILE="zentrum"  # alternativ: "kurs"
MQTT_PROFILE="emqx"     # alternativ: "kurs"
```

`zentrum` verwendet `WIFI_SSID` und `WIFI_PASSWORD`; `kurs` verwendet
`KURS_SSID` und `KURS_PASSWORD`. Beim Broker verwendet `emqx` die Werte
`MQTT_HOST`, `MQTT_USER`, `MQTT_PASSWORD` und `MQTT_USE_TLS`. Das Kursprofil
setzt automatisch Host `158.180.44.197`, Port `1883`, Benutzer `bobm` und
TLS aus; dafür muss nur `MQTT_KURS_BROKER_PASS` eingetragen werden.

Beim Start zeigt die serielle Konsole die ausgewählten Profilnamen, aber keine
Passwörter. Ein einmaliger Build mit abweichender Auswahl ist ebenfalls möglich:

```bash
WIFI_PROFILE=kurs MQTT_PROFILE=kurs pio run
```

## MQTT

Der Kurs-Broker ist `158.180.44.197:1883` (ohne TLS). Die Firmware publiziert
minütlich JSON-Nachrichten mit UTC-Zeitstempel auf:

- `iiot/group/<gruppe>/sensor/temperature/state`
- `iiot/group/<gruppe>/sensor/humidity/state`
- `iiot/group/<gruppe>/sensor/hygrometer-1/state`
- `iiot/group/<gruppe>/sensor/hygrometer-2/state`
- `iiot/group/<gruppe>/status` (retained; Last Will `offline`)

Die Messwerte verwenden die Felder `timestamp`, `sensor_id`, `value`, `unit`
und `status`. Das Sendeintervall beträgt standardmäßig 60 Sekunden.

Für den EMQX-Cloud-Broker können in der lokalen `.env` diese Werte verwendet
werden:

```text
MQTT_HOST="e2f0071d.ala.eu-central-1.emqxsl.com"
MQTT_USER="IIoT"
MQTT_PASSWORD="<EMQX-Passwort>"
MQTT_USE_TLS="true"
```

`MQTT_USE_TLS` ist standardmäßig `false`; dadurch bleiben der bisherige
Kurs-Broker und die bisherigen Einstellungen für die Abgabe erhalten. Bei
`true` nutzt die Firmware automatisch TLS auf Port 8883. Der TLS-Kanal wird
verschlüsselt aufgebaut; die Host-Zertifikatsprüfung ist in dieser Variante
deaktiviert, da das Broker-CA-Zertifikat nicht im Projekt hinterlegt ist.

## REST-API

Nach der WLAN-Verbindung ist die API unter der IP-Adresse des ESP32 erreichbar:

- `GET /` – einfacher Erreichbarkeitstest
- `GET /config` – aktuelle Gerätekonfiguration
- `POST /config` – setzt `reading_interval_seconds` (2 bis 86400 Sekunden)
- `GET /status` – WLAN-, MQTT- und IP-Status

Beispiel für ein neues 10-Sekunden-Intervall unter Windows:

```bat
curl -X POST http://<ip-des-esp32>/config ^
  -H "Content-Type: application/json" ^
  -d "{\"reading_interval_seconds\":10}"
```

## Fehlerbehebung

- **DHT20 nicht erkannt:** SDA/SCL, Versorgung und I²C-Pull-ups prüfen.
  Der aktuell unterstützte Sensor ist ein **DHT20**. Ein echter **DHT11**
  verwendet kein I²C und kann mit dieser Firmware nicht an SDA/SCL gelesen
  werden; dafür wären eine One-Wire-Datenleitung und eine passende DHT11-
  Bibliothek erforderlich.
- **Hygrometer-Wert unplausibel:** sicherstellen, dass das Signal maximal 3,3 V
  beträgt. Die Kalibrierpunkte stehen als `HYGRO_ADC_DRY` und
  `HYGRO_ADC_WET` in `src/main.cpp`.
- **MQTT-Verbindung schlägt fehl:** Broker-Zugangsdaten und insbesondere das
  in der Vorlesung bekanntgegebene Passwort prüfen.

---

# Datei: `src/esp32_firmware/config.h`

```cpp
#ifndef CONFIG_H
#define CONFIG_H

/*
 * =====================================================================================
 *
 * Filename:  config.h
 *
 * Description:  Konfigurationsdatei für WiFi, MQTT und Sensor-Metadaten.
 * Hier werden alle benutzerspezifischen Einstellungen und
 * Anmeldeinformationen zentral verwaltet.
 *
 * =====================================================================================
 */

// ----- WLAN-EINSTELLUNGEN -----
// Tragen Sie hier die Zugangsdaten für Ihr WLAN-Netzwerk ein.
const char* WIFI_SSID = "Your_WiFi_SSID";
const char* WIFI_PASSWORD = "Your_WiFi_Password";


// ----- MQTT BROKER EINSTELLUNGEN -----
// Tragen Sie hier die Daten Ihres MQTT-Brokers ein.
const char* MQTT_BROKER_HOST = "158.180.44.197";
const int   MQTT_BROKER_PORT = 1883; // Kurs-Broker: unverschlüsselt (MQTTS mit TLS wäre 8883)
const char* MQTT_CLIENT_ID_PREFIX = "ESP32_Sensor_"; // Präfix für die Client-ID


// ----- ZERTIFIKATE FÜR MQTTS (Broker CA Certificate) -----
// Ersetzen Sie den Inhalt zwischen R"EOF(...)EOF" durch das tatsächliche
// CA-Zertifikat Ihres MQTT-Brokers im PEM-Format.
// Dieses Zertifikat stellt sicher, dass die Verbindung zum richtigen Broker aufgebaut wird.
const char* MQTT_BROKER_CA_CERT = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
-----END CERTIFICATE-----
)EOF";


// ----- STANDARD-SENSOR-METADATEN -----
// Diese Werte dienen als Standard für die Sensor-Metadaten.
// Sie können für jeden spezifischen Sensor im Hauptprogramm überschrieben werden.
const char* DEFAULT_SENSOR_LOCATION = "Labor 1";
const char* DEFAULT_SENSOR_DESCRIPTION = "Allgemeiner Umgebungssensor";

#endif // CONFIG_H
```

---

# Datei: `src/esp32_firmware/include/config_secure.h`

```cpp
#ifndef CONFIG_SECURE_H
#define CONFIG_SECURE_H

// Dieser Header ist für Port-Definitionen und große, statische Daten wie Zertifikate gedacht.

// Kurs-Broker: unverschlüsselt auf Port 1883 (siehe docs/iot-specs/conventions.md)
const int MQTT_INSECURE_PORT = 1883;
// Nur relevant, falls ein Broker mit TLS genutzt wird (useSecureMqtt = true)
const int MQTT_SECURE_PORT = 8883;

const char* MQTT_CLIENT_ID_PREFIX = "ESP32_Sensor_"; // Präfix für die Client-ID

const char* MQTT_BROKER_CA_CERT = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
...
-----END CERTIFICATE-----
)EOF";

#endif
```

---

# Datei: `src/esp32_firmware/load_env.py`

```python
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
```

---

# Datei: `src/esp32_firmware/platformio.ini`

```ini
[env:esp32-c3]
platform = espressif32
board = esp32-c3-devkitm-1
framework = arduino
monitor_speed = 115200
lib_deps =
  knolleary/PubSubClient@^2.8
  bblanchon/ArduinoJson@^7
build_flags =
  -D ARDUINO_USB_MODE=1
  -D ARDUINO_USB_CDC_ON_BOOT=1
extra_scripts = pre:load_env.py
```

---

# Datei: `src/esp32_firmware/src/Sensor.h`

```cpp
#ifndef SENSOR_H
#define SENSOR_H

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <WebServer.h>
#include <Preferences.h>
#include "config_secure.h" // Inkludiert Zertifikat und Port-Definitionen

// Globale Objekte, da sie von der Basisklasse genutzt werden
extern WiFiClient espClient;              // Unverschlüsselt (Port 1883)
extern WiFiClientSecure espClientSecure;  // TLS (Port 8883)
extern PubSubClient mqttClient;
extern WebServer server;
extern Preferences preferences;

class Sensor {
protected:
    String sensorId;
    String sensorName;
    unsigned long sendInterval;
    unsigned long lastSendTime = 0;
    String mqttTopicData;
    String mqttTopicMeta;
    bool useSecureConnection; // Das neue Flag für MQTTS

    struct SensorMetadata {
        String type, unit, location, description;
        float min_value, max_value;
    } metadata;

public:
    // Der Konstruktor nimmt nun das Flag für die Verbindungsart entgegen
    Sensor(String type, String unit, float minVal, float maxVal, String loc, String desc, bool isSecure) {
        useSecureConnection = isSecure;

        // TODO: Die Client-ID muss am Broker eindeutig sein – z.B. aus der MAC-Adresse
        // oder dem Gruppennamen ableiten. Verbinden sich zwei Geräte mit derselben ID,
        // trennt der Broker jeweils das zuvor verbundene Gerät.
        sensorId = String(MQTT_CLIENT_ID_PREFIX) + "TODO-eindeutige-ID";

        preferences.begin("sensor_config", false);
        sensorName = preferences.getString("sensorName", "DefaultSensor");
        sendInterval = preferences.getULong("sendInterval", 5000);
        preferences.end();

        metadata.type = type;
        metadata.unit = unit;
        metadata.min_value = minVal;
        metadata.max_value = maxVal;
        metadata.location = loc;
        metadata.description = desc;

        mqttTopicData = "iiot/sensors/" + sensorId + "/data";
        mqttTopicMeta = "iiot/sensors/" + sensorId + "/meta";
    }

    virtual ~Sensor() {}

    // Virtuelle Funktionen müssen von der abgeleiteten Klasse implementiert werden
    virtual float readSensorValue() = 0;
    virtual void buildSensorDataJson(JsonDocument& doc, float value) = 0;

    void setupWifiAndMqtt() {
        Serial.print("Connecting to WiFi: ");
        Serial.println(WIFI_SSID); // Kommt aus platformio.ini
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD); // Kommt aus platformio.ini
        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
            Serial.print(".");
        }
        Serial.println("\nWiFi connected. IP: " + WiFi.localIP().toString());

        // Logik für sichere vs. unsichere Verbindung
        if (useSecureConnection) {
            Serial.println("Setting up secure MQTTS connection.");
            espClientSecure.setCACert(MQTT_BROKER_CA_CERT); // Zertifikat aus config_secure.h
            mqttClient.setClient(espClientSecure);
            mqttClient.setServer(MQTT_BROKER_HOST, MQTT_SECURE_PORT); // Sicherer Port
        } else {
            Serial.println("Setting up insecure MQTT connection. NO CERTIFICATE WILL BE USED.");
            mqttClient.setClient(espClient);
            mqttClient.setServer(MQTT_BROKER_HOST, MQTT_INSECURE_PORT); // Unsicherer Port
        }
        
        mqttClient.setCallback(mqttCallback);
    }

    void reconnectMqtt() {
        while (!mqttClient.connected()) {
            Serial.print("Attempting MQTT connection...");
            // MQTT_USER und MQTT_PASSWORD kommen aus platformio.ini (.env)
            if (mqttClient.connect(sensorId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
                Serial.println("connected!");
                publishMetadata();
            } else {
                Serial.print("failed, rc=");
                Serial.print(mqttClient.state());
                Serial.println(" try again in 5 seconds");
                delay(5000);
            }
        }
    }

    void loop() {
        if (!mqttClient.connected()) {
            reconnectMqtt();
        }
        mqttClient.loop();

        if (millis() - lastSendTime > sendInterval) {
            float value = readSensorValue();
            if (!isnan(value)) {
                publishSensorData(value);
            }
            lastSendTime = millis();
        }
    }

    // Die restlichen Funktionen (publishSensorData, publishMetadata, REST-API, etc.)
    // bleiben im Wesentlichen gleich wie im ursprünglichen Code.
    // (Aus Platzgründen hier nicht erneut aufgeführt)
    void publishSensorData(float value);
    void publishMetadata();
    void setupRestApi();
    void handleRestApi();

private:
    void handleGetSettings();
    void handlePostSettings();
    static void mqttCallback(char* topic, byte* payload, unsigned int length);
};

// Implementierungen der verbleibenden Funktionen müssen in einer .cpp-Datei sein,
// idealerweise in Sensor.cpp, oder zur Vereinfachung direkt in main.cpp.

#endif // SENSOR_H
```

---

# Datei: `src/esp32_firmware/src/main.cpp`

```cpp
#include <Arduino.h>
#include "env_config.h"
#include <ArduinoJson.h>
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <Wire.h>
#include <time.h>

// Hardware from HygroMQTT:
// DHT20: SDA GPIO 8, SCL GPIO 9
// Analog hygrometers: GPIO 0 (A0) and GPIO 1
constexpr uint8_t DHT20_SDA_PIN = 8;
constexpr uint8_t DHT20_SCL_PIN = 9;
constexpr uint8_t HYGROMETER_1_PIN = 0;
constexpr uint8_t HYGROMETER_2_PIN = 1;
constexpr uint8_t DHT20_I2C_ADDR = 0x38;

// Credentials are injected from the ignored .env file by load_env.py.
constexpr char WIFI_SSID_VALUE[] = WIFI_SSID;
constexpr char WIFI_PASSWORD_VALUE[] = WIFI_PASSWORD;
constexpr char WIFI_PROFILE_VALUE[] = WIFI_PROFILE_NAME;

// Set the group slug to the participating members' lowercase surnames.
constexpr char MQTT_GROUP[] = "unterhuber-brachmann-reimeir-noessing";
constexpr char DEVICE_ID[] = "yourmuesli-innsbruck-01";
constexpr char MQTT_HOST_VALUE[] = MQTT_BROKER_HOST;
constexpr bool MQTT_USE_TLS_VALUE =
    (MQTT_USE_TLS[0] == '1' || MQTT_USE_TLS[0] == 'y' || MQTT_USE_TLS[0] == 'Y' ||
     MQTT_USE_TLS[0] == 't' || MQTT_USE_TLS[0] == 'T');
constexpr uint16_t MQTT_PORT = MQTT_USE_TLS_VALUE ? 8883 : 1883;
constexpr char MQTT_USER_VALUE[] = MQTT_USER;
constexpr char MQTT_PASSWORD_VALUE[] = MQTT_PASSWORD;
constexpr char MQTT_PROFILE_VALUE[] = MQTT_PROFILE_NAME;

constexpr unsigned long DEFAULT_INTERVAL_MS = 60000;
constexpr unsigned long WIFI_RETRY_MS = 10000;
constexpr unsigned long MQTT_RETRY_MS = 5000;
constexpr unsigned long DEBUG_STATUS_MS = 2000;
constexpr unsigned long DHT20_MEASUREMENT_DELAY_MS = 85;
constexpr int HYGRO_ADC_DRY = 3000;
constexpr int HYGRO_ADC_WET = 900;

WiFiClient wifiClient;
WiFiClientSecure secureClient;
PubSubClient mqttClient(wifiClient);
WebServer server(80);

String temperatureTopic;
String humidityTopic;
String hygrometer1Topic;
String hygrometer2Topic;
String statusTopic;
unsigned long readingIntervalMs = DEFAULT_INTERVAL_MS;
unsigned long lastReading = 0;
unsigned long lastWiFiAttempt = 0;
unsigned long lastMqttAttempt = 0;
unsigned long lastDebugStatus = 0;
bool dht20Detected = false;
bool lastPublishSuccessful = false;
unsigned long lastPublishAtMs = 0;
float lastTemperature = NAN;
float lastHumidity = NAN;
float lastHygrometer1 = NAN;
float lastHygrometer2 = NAN;

String isoUtcNow() {
  time_t now = time(nullptr);
  struct tm utc {};
  gmtime_r(&now, &utc);
  char timestamp[25];
  strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", &utc);
  return String(timestamp);
}

void publishStatus(const char* status) {
  if (!mqttClient.connected()) {
    Serial.println("[MQTT] Status skipped: client is not connected");
    return;
  }

  JsonDocument document;
  document["status"] = status;
  document["timestamp"] = isoUtcNow();
  document["sensor_id"] = DEVICE_ID;
  String payload;
  serializeJson(document, payload);
  const bool published = mqttClient.publish(statusTopic.c_str(), payload.c_str(), true);
  Serial.printf("[MQTT] Status %s: %s -> %s\n",
                published ? "published" : "failed",
                statusTopic.c_str(), payload.c_str());
}

bool publishReading(const char* topic, float value, const char* unit) {
  if (!mqttClient.connected()) {
    Serial.printf("[MQTT] Reading skipped: client is not connected (%s)\n", topic);
    return false;
  }

  JsonDocument document;
  document["timestamp"] = isoUtcNow();
  document["sensor_id"] = DEVICE_ID;
  document["value"] = value;
  document["unit"] = unit;
  document["status"] = "ok";
  String payload;
  serializeJson(document, payload);

  const bool published = mqttClient.publish(topic, payload.c_str(), true);
  Serial.printf("[MQTT] Reading %s: %s -> %s\n",
                published ? "published" : "failed", topic, payload.c_str());
  return published;
}

bool clockIsSynchronized() {
  // 2024-01-01. Prevent invalid 1970 timestamps before NTP has completed.
  return time(nullptr) >= 1704067200;
}

bool readDht20(float& humidity, float& temperature) {
  if (!dht20Detected) {
    return false;
  }

  Wire.beginTransmission(DHT20_I2C_ADDR);
  Wire.write(0xAC);
  Wire.write(0x33);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) {
    return false;
  }

  delay(DHT20_MEASUREMENT_DELAY_MS);
  if (Wire.requestFrom(DHT20_I2C_ADDR, static_cast<uint8_t>(7)) != 7) {
    return false;
  }

  uint8_t data[7];
  for (uint8_t& byte : data) {
    byte = Wire.read();
  }
  if ((data[0] & 0x80) != 0) {
    return false;
  }

  const uint32_t rawHumidity =
      (static_cast<uint32_t>(data[1]) << 12) |
      (static_cast<uint32_t>(data[2]) << 4) |
      (data[3] >> 4);
  const uint32_t rawTemperature =
      ((static_cast<uint32_t>(data[3]) & 0x0F) << 16) |
      (static_cast<uint32_t>(data[4]) << 8) |
      data[5];

  humidity = (rawHumidity / 1048576.0f) * 100.0f;
  temperature = (rawTemperature / 1048576.0f) * 200.0f - 50.0f;
  return humidity >= 0.0f && humidity <= 100.0f &&
         temperature >= -40.0f && temperature <= 85.0f;
}

float readHygrometer(uint8_t pin) {
  constexpr uint8_t sampleCount = 8;
  uint32_t sum = 0;
  for (uint8_t sample = 0; sample < sampleCount; ++sample) {
    sum += analogRead(pin);
    delay(2);
  }

  const int raw = static_cast<int>(sum / sampleCount);
  const float percentage =
      (static_cast<float>(HYGRO_ADC_DRY - raw) /
       static_cast<float>(HYGRO_ADC_DRY - HYGRO_ADC_WET)) * 100.0f;
  return constrain(percentage, 0.0f, 100.0f);
}

void publishSensorData() {
  if (!mqttClient.connected()) {
    Serial.println("[Sensor] Measurement skipped: MQTT is not connected");
    return;
  }
  if (!clockIsSynchronized()) {
    Serial.println("[NTP] Measurement postponed until the clock is synchronized");
    return;
  }

  float humidity = NAN;
  float temperature = NAN;
  const bool dhtOk = readDht20(humidity, temperature);
  const float hygrometer1 = readHygrometer(HYGROMETER_1_PIN);
  const float hygrometer2 = readHygrometer(HYGROMETER_2_PIN);
  lastHumidity = humidity;
  lastTemperature = temperature;
  lastHygrometer1 = hygrometer1;
  lastHygrometer2 = hygrometer2;

  Serial.printf("[Sensor] hygrometer 1: %.2f %% (GPIO %u), hygrometer 2: %.2f %% (GPIO %u)\n",
                hygrometer1, HYGROMETER_1_PIN, hygrometer2, HYGROMETER_2_PIN);
  if (dhtOk) {
    const bool temperaturePublished = publishReading(temperatureTopic.c_str(), temperature, "°C");
    const bool humidityPublished = publishReading(humidityTopic.c_str(), humidity, "%");
    publishStatus("ok");
    lastPublishSuccessful = temperaturePublished && humidityPublished;
    Serial.printf("[Sensor] %.2f °C, %.2f %% RH, hygrometer 1: %.2f %%, hygrometer 2: %.2f %%\n",
                  temperature, humidity, hygrometer1, hygrometer2);
  } else {
    publishStatus("error");
    lastPublishSuccessful = false;
    Serial.printf("[DHT20] Read failed (I2C address 0x%02X)\n", DHT20_I2C_ADDR);
  }
  const bool hygrometer1Published = publishReading(hygrometer1Topic.c_str(), hygrometer1, "%");
  const bool hygrometer2Published = publishReading(hygrometer2Topic.c_str(), hygrometer2, "%");
  lastPublishSuccessful = lastPublishSuccessful && hygrometer1Published && hygrometer2Published;
  lastPublishAtMs = millis();
}

void handleGetConfig() {
  JsonDocument document;
  document["device_id"] = DEVICE_ID;
  document["reading_interval_seconds"] = readingIntervalMs / 1000;
  document["location"] = "Produktionshalle 1, Innsbruck";
  String response;
  serializeJson(document, response);
  server.send(200, "application/json", response);
}

void handlePostConfig() {
  JsonDocument document;
  const DeserializationError error = deserializeJson(document, server.arg("plain"));
  if (error) {
    server.send(400, "application/json", "{\"error\":\"invalid JSON\"}");
    return;
  }

  if (!document["reading_interval_seconds"].is<unsigned long>()) {
    server.send(400, "application/json",
                "{\"error\":\"reading_interval_seconds must be an integer\"}");
    return;
  }
  if (document.size() != 1) {
    server.send(400, "application/json",
                "{\"error\":\"unknown configuration field\"}");
    return;
  }

  const unsigned long seconds = document["reading_interval_seconds"];
  if (seconds < 2 || seconds > 86400) {
    server.send(400, "application/json",
                "{\"error\":\"interval must be between 2 and 86400 seconds\"}");
    return;
  }

  readingIntervalMs = seconds * 1000UL;
  server.send(200, "application/json", "{\"status\":\"updated\"}");
}

void handleStatus() {
  JsonDocument document;
  document["device_id"] = DEVICE_ID;
  document["wifi_connected"] = WiFi.status() == WL_CONNECTED;
  document["mqtt_connected"] = mqttClient.connected();
  document["clock_synchronized"] = clockIsSynchronized();
  document["ip"] = WiFi.localIP().toString();
  document["uptime_seconds"] = millis() / 1000UL;
  document["last_publish_successful"] = lastPublishSuccessful;
  if (lastPublishAtMs > 0) {
    document["seconds_since_last_publish"] = (millis() - lastPublishAtMs) / 1000UL;
  } else {
    document["seconds_since_last_publish"] = nullptr;
  }
  JsonObject readings = document["last_readings"].to<JsonObject>();
  if (!isnan(lastTemperature)) readings["temperature_c"] = lastTemperature;
  if (!isnan(lastHumidity)) readings["humidity_percent"] = lastHumidity;
  if (!isnan(lastHygrometer1)) readings["hygrometer_1_percent"] = lastHygrometer1;
  if (!isnan(lastHygrometer2)) readings["hygrometer_2_percent"] = lastHygrometer2;
  String response;
  serializeJson(document, response);
  server.send(200, "application/json", response);
}

void handleNotFound() {
  const String uri = server.uri();
  if (uri == "/" || uri == "/config" || uri == "/status") {
    server.sendHeader("Allow", uri == "/config" ? "GET, POST" : "GET");
    server.send(405, "application/json", "{\"error\":\"method not allowed\"}");
    return;
  }
  server.send(404, "application/json", "{\"error\":\"not found\"}");
}

void setupRestApi() {
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/plain",
                "yourmuesli ESP32 sensor is running\n");
  });
  server.on("/config", HTTP_GET, handleGetConfig);
  server.on("/config", HTTP_POST, handlePostConfig);
  server.on("/status", HTTP_GET, handleStatus);
  server.onNotFound(handleNotFound);
  server.begin();
}

void connectWiFi() {
  Serial.printf("[WiFi] Connecting to SSID \"%s\"\n", WIFI_SSID_VALUE);
  WiFi.mode(WIFI_STA);
  if (!WiFi.setTxPower(WIFI_POWER_8_5dBm)) {
    Serial.println("[WiFi] Failed to set transmit power");
  }
  WiFi.setAutoReconnect(true);
  WiFi.disconnect();
  delay(100);
  WiFi.begin(WIFI_SSID_VALUE, WIFI_PASSWORD_VALUE);
}

void scanI2cBus() {
  Serial.printf("[I2C] Scanning SDA=%u, SCL=%u...\n", DHT20_SDA_PIN, DHT20_SCL_PIN);
  uint8_t found = 0;
  for (uint8_t address = 1; address < 127; ++address) {
    Wire.beginTransmission(address);
    const uint8_t error = Wire.endTransmission();
    if (error == 0) {
      Serial.printf("[I2C] Device found at 0x%02X%s\n", address,
                    address == DHT20_I2C_ADDR ? " (expected DHT20)" : "");
      ++found;
    }
  }
  if (found == 0) {
    Serial.println("[I2C] No devices found. Check power, GND, SDA/SCL and pull-ups.");
  }
}

const char* wifiStatusText(wl_status_t status) {
  switch (status) {
    case WL_CONNECTED: return "CONNECTED";
    case WL_NO_SSID_AVAIL: return "NO_SSID";
    case WL_CONNECT_FAILED: return "CONNECT_FAILED";
    case WL_CONNECTION_LOST: return "CONNECTION_LOST";
    case WL_DISCONNECTED: return "DISCONNECTED";
    default: return "OTHER";
  }
}

void printDebugStatus() {
  const wl_status_t status = WiFi.status();
  Serial.printf("[DEBUG] WiFi=%s (%d), RSSI=%d dBm, IP=%s, MQTT=%s, free heap=%lu\n",
                wifiStatusText(status), status,
                status == WL_CONNECTED ? WiFi.RSSI() : 0,
                WiFi.localIP().toString().c_str(),
                mqttClient.connected() ? "CONNECTED" : "DISCONNECTED",
                static_cast<unsigned long>(ESP.getFreeHeap()));
}

void connectMqtt() {
  if (WiFi.status() != WL_CONNECTED || mqttClient.connected()) {
    return;
  }

  const String clientId = "esp32c3-" + String(static_cast<uint32_t>(ESP.getEfuseMac()), HEX);
  Serial.printf("[MQTT] Connecting to %s as %s\n", MQTT_HOST_VALUE, clientId.c_str());
  if (mqttClient.connect(clientId.c_str(), MQTT_USER_VALUE, MQTT_PASSWORD_VALUE,
                         statusTopic.c_str(), 1, true, "{\"status\":\"offline\"}")) {
    Serial.println("[MQTT] Connected");
    publishStatus("ok");
    lastReading = millis() - readingIntervalMs;
  } else {
    Serial.printf("[MQTT] Connection failed, state=%d\n", mqttClient.state());
  }
}

void initializeDht20() {
  Wire.begin(DHT20_SDA_PIN, DHT20_SCL_PIN);
  Wire.setClock(100000);
  scanI2cBus();
  Wire.beginTransmission(DHT20_I2C_ADDR);
  dht20Detected = Wire.endTransmission() == 0;
  Serial.println(dht20Detected ? "[DHT20] Detected" : "[DHT20] Not detected");
}

void setup() {
  Serial.begin(115200);
  const unsigned long serialWaitStart = millis();
  while (!Serial && millis() - serialWaitStart < 5000) {
    delay(10);
  }
  delay(200);
  Serial.println("\n========== IIoT ESP32 SENSOR ==========");
  Serial.println("[BOOT] Debug logging enabled");
  Serial.println("[BOOT] This firmware supports a DHT20 over I2C, not a DHT11.");
  Serial.printf("[BOOT] Profiles: WiFi=%s, MQTT=%s\n",
                WIFI_PROFILE_VALUE, MQTT_PROFILE_VALUE);

  temperatureTopic = "iiot/group/" + String(MQTT_GROUP) +
                     "/sensor/temperature/state";
  humidityTopic = "iiot/group/" + String(MQTT_GROUP) +
                  "/sensor/humidity/state";
  hygrometer1Topic = "iiot/group/" + String(MQTT_GROUP) +
                     "/sensor/hygrometer-1/state";
  hygrometer2Topic = "iiot/group/" + String(MQTT_GROUP) +
                     "/sensor/hygrometer-2/state";
  statusTopic = "iiot/group/" + String(MQTT_GROUP) + "/status";
  Serial.printf("[MQTT] Temperature topic: %s\n", temperatureTopic.c_str());
  Serial.printf("[MQTT] Humidity topic: %s\n", humidityTopic.c_str());
  Serial.printf("[MQTT] Hygrometer 1 topic: %s\n", hygrometer1Topic.c_str());
  Serial.printf("[MQTT] Hygrometer 2 topic: %s\n", hygrometer2Topic.c_str());
  Serial.printf("[MQTT] Status topic: %s\n", statusTopic.c_str());

  analogReadResolution(12);
  analogSetPinAttenuation(HYGROMETER_1_PIN, ADC_11db);
  analogSetPinAttenuation(HYGROMETER_2_PIN, ADC_11db);
  initializeDht20();
  connectWiFi();
  lastWiFiAttempt = millis() - WIFI_RETRY_MS;
  lastDebugStatus = millis() - DEBUG_STATUS_MS;
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");

  if (MQTT_USE_TLS_VALUE) {
    // The EMQX Cloud certificate is validated by the broker hostname.
    secureClient.setInsecure();
    mqttClient.setClient(secureClient);
    Serial.println("[MQTT] TLS enabled");
  } else {
    mqttClient.setClient(wifiClient);
    Serial.println("[MQTT] TLS disabled (course-broker fallback)");
  }
  mqttClient.setServer(MQTT_HOST_VALUE, MQTT_PORT);
  setupRestApi();
}

void loop() {
  const unsigned long now = millis();

  if (WiFi.status() != WL_CONNECTED) {
    if (now - lastWiFiAttempt >= WIFI_RETRY_MS) {
      lastWiFiAttempt = now;
      connectWiFi();
    }
  } else if (!mqttClient.connected()) {
    if (now - lastMqttAttempt >= MQTT_RETRY_MS) {
      lastMqttAttempt = now;
      connectMqtt();
    }
  } else {
    mqttClient.loop();
  }

  if (now - lastReading >= readingIntervalMs) {
    lastReading = now;
    publishSensorData();
  }
  if (now - lastDebugStatus >= DEBUG_STATUS_MS) {
    lastDebugStatus = now;
    printDebugStatus();
  }

  server.handleClient();
  delay(10);
}
```

---

# Datei: `src/esp32_firmware/src/sensors/my_sensor.h`

```cpp
#ifndef MY_SENSOR_H
#define MY_SENSOR_H

#include "Sensor.h"
#include <DHT.h>

// Konfiguration für den konkreten Sensor
#define DHT_SENSOR_PIN 4
#define DHT_SENSOR_TYPE DHT11

class MyTempSensor : public Sensor {
private:
    DHT dht; // Das sensorspezifische Objekt

public:
    // Der Konstruktor ruft den Basis-Konstruktor auf und leitet alle Infos weiter
    MyTempSensor(String location, String description, bool useSecureMqtt)
        : Sensor("temperature", "°C", -10.0, 50.0, location, description, useSecureMqtt),
          dht(DHT_SENSOR_PIN, DHT_SENSOR_TYPE)
    {
        Serial.println("Initializing DHT11 sensor...");
        dht.begin();
    }

    // Implementierung der reinen virtuellen Funktionen der Basisklasse
    float readSensorValue() override {
        float temp = dht.readTemperature();
        if (isnan(temp)) {
            Serial.println("Failed to read from DHT sensor!");
            return NAN; // Gibt "Not a Number" zurück, um Fehler zu signalisieren
        }
        return temp;
    }

    void buildSensorDataJson(JsonDocument& doc, float value) override {
        // Fügt die spezifischen Daten zum JSON-Payload hinzu
        doc["temperature"] = value;
        // Optional auch die Luftfeuchtigkeit hinzufügen
        float humidity = dht.readHumidity();
        if (!isnan(humidity)) {
            doc["humidity"] = humidity;
        }
    }
};

#endif // MY_SENSOR_H
```

---

# Datei: `src/raspi_firmware/code.py`

```python
# code.py

# ===================================================================
# Haupt-Anwendung für das yourmuesli.at IoT Environmental Monitoring
#
# Autor: Ihr Team
# Datum: 02.09.2025
#
# Hardware: Raspberry Pi Pico W
# Sensor: DHT11 (Temperatur & Luftfeuchtigkeit)
# Software: CircuitPython
# ===================================================================

# ----------- Bibliotheken importieren -----------
# Hier werden später alle benötigten CircuitPython-Bibliotheken importiert
# z.B. import board, time, wifi, adafruit_dht, etc.


# ===================================================================
# KLASSE: ConfigManager
# ===================================================================
class ConfigManager:
    """
    Verwaltet das Laden und Speichern der Konfiguration aus der 'settings.toml'.

    Hinweis: CircuitPython bringt kein 'toml'-Modul mit. Ein minimaler Parser
    liegt unter lib/toml.py (mit 'import toml' nutzbar), dazu den Ordner 'lib'
    auf das CIRCUITPY-Laufwerk kopieren.
    """

    def __init__(self, filepath: str):
        """
        Initialisiert den ConfigManager.

        :param filepath: Der Pfad zur Konfigurationsdatei (z.B. "settings.toml").
        """
        pass

    def load_settings(self) -> dict:
        """
        Lädt die Einstellungen aus der TOML-Datei.

        :return: Ein Dictionary mit allen geladenen Einstellungen.
        """
        pass

    def save_settings(self, settings: dict):
        """
        Speichert Änderungen zurück in die TOML-Datei und startet den
        Mikrocontroller neu, um die neuen Einstellungen zu übernehmen.

        Achtung:
        - Standardmäßig kann CircuitPython nicht auf das eigene Dateisystem
          schreiben (nur der angeschlossene Computer per USB). Dafür muss in
          einer 'boot.py' das Dateisystem mit storage.remount("/", readonly=False)
          beschreibbar gemacht werden - danach kann der Computer nicht mehr
          schreiben. Überlegen Sie, wie Sie zwischen beiden Modi wechseln
          (z.B. über einen Taster/Pin, der in boot.py abgefragt wird).
        - toml.dump() schreibt nur "schluessel = wert"-Zeilen, Kommentare in
          der settings.toml gehen dabei verloren.

        :param settings: Das Dictionary mit den zu speichernden Einstellungen.
        """
        pass


# ===================================================================
# KLASSE: NetworkManager
# ===================================================================
class NetworkManager:
    """
    Kümmert sich um die Verbindung zum WLAN-Netzwerk.
    """

    def __init__(self, ssid: str, password: str):
        """
        Initialisiert den NetworkManager mit den WLAN-Zugangsdaten.

        :param ssid: Der Name des WLAN-Netzwerks (SSID).
        :param password: Das Passwort für das WLAN-Netzwerk.
        """
        pass

    def connect(self) -> bool:
        """
        Stellt die Verbindung zum WLAN her. Versucht es bei einem Fehler
        mehrfach, bevor aufgegeben wird.

        :return: True bei erfolgreicher Verbindung, ansonsten False.
        """
        pass

    def is_connected(self) -> bool:
        """
        Prüft den aktuellen Verbindungsstatus.

        :return: True, wenn eine WLAN-Verbindung besteht, ansonsten False.
        """
        pass

    def get_ip(self) -> str:
        """
        Gibt die aktuell zugewiesene IP-Adresse des Geräts zurück.

        :return: Die IP-Adresse als String (z.B. "192.168.1.100").
        """
        pass


# ===================================================================
# KLASSE: Sensor
# ===================================================================
class Sensor:
    """
    Kapselt die Logik zum Auslesen des DHT11-Sensors.
    """

    def __init__(self, pin_number: int):
        """
        Initialisiert den Sensor am angegebenen GPIO-Pin.

        :param pin_number: Die Nummer des GPIO-Pins (z.B. 22 für GP22).
        """
        pass

    def read_data(self) -> dict | None:
        """
        Liest Temperatur und Luftfeuchtigkeit vom Sensor.

        :return: Ein Dictionary wie {'temperature': 22.5, 'humidity': 45.8}
                 oder None, falls das Auslesen fehlschlägt.
        """
        pass


# ===================================================================
# KLASSE: MqttClient
# ===================================================================
class MqttClient:
    """
    Verwaltet die Kommunikation mit dem zentralen MQTT-Broker.
    """

    def __init__(self, config: dict):
        """
        Initialisiert den MQTT-Client mit den Broker-Details aus der Konfiguration.

        :param config: Ein Dictionary mit den MQTT-Einstellungen.
        """
        pass

    def connect(self):
        """
        Verbindet sich mit dem MQTT-Broker und setzt eine "Last Will and Testament"
        Nachricht mit dem Status "offline", die der Broker sendet, falls das Gerät
        unerwartet die Verbindung verliert.
        """
        pass

    def publish_telemetry(self, data: dict):
        """
        Formatiert die Sensordaten in ein JSON-Payload und sendet sie
        an das definierte Telemetrie-Topic.

        :param data: Das Dictionary mit den Sensordaten.
        """
        pass

    def publish_status(self, status: str):
        """
        Sendet eine einfache Statusnachricht an das definierte Status-Topic.
        Erlaubte Werte laut docs/iot-specs/conventions.md: "ok", "error", "offline".

        :param status: Die zu sendende Statusnachricht ("ok", "error" oder "offline").
        """
        pass

    def loop(self):
        """
        Hält die MQTT-Verbindung aktiv. Muss regelmäßig in der Hauptschleife
        aufgerufen werden.
        """
        pass


# ===================================================================
# KLASSE: WebServer
# ===================================================================
class WebServer:
    """
    Stellt die HTTP-Schnittstelle zur Fernkonfiguration bereit.

    Die Endpunkte und das JSON-Format sind in docs/iot-specs/openapi.yaml
    und docs/iot-specs/conventions.md festgelegt:
      GET  /config  -> aktuelle Konfiguration als JSON
      POST /config  <- neue Werte als JSON (z.B. {"reading_interval_seconds": 120})
      GET  /status  -> Gerätestatus als JSON (Felder werden in der Gesamtgruppe festgelegt)
    Eine zusätzliche HTML-Seite für Menschen (z.B. unter "/") ist optional.

    Hinweise:
    - poll() darf die Hauptschleife nicht blockieren, sonst bleibt MQTT stehen.
      Stichworte: socket.setblocking(False), accept() liefert dann OSError
      (EAGAIN), wenn gerade keine Anfrage anliegt.
    - Nach einem Neustart per Auto-Reload ist Port 80 oft noch belegt.
      Stichworte: SO_REUSEADDR, oder start() bei Fehler später erneut versuchen.
    """

    def __init__(self, config_manager: ConfigManager):
        """
        Initialisiert den Webserver.

        :param config_manager: Eine Instanz des ConfigManagers, um Einstellungen
                               zu lesen und zu speichern.
        """
        pass

    def start(self):
        """
        Startet den Webserver, sodass er auf Anfragen lauscht.
        """
        pass

    def poll(self):
        """
        Verarbeitet eine einzelne anstehende HTTP-Anfrage. Muss in der
        Hauptschleife des Programms aufgerufen werden.
        """
        pass

    def _handle_get_request(self, request):
        """
        Interne Methode: Bearbeitet GET-Anfragen. Liefert je nach Pfad die
        Konfiguration (/config) oder den Status (/status) als JSON aus,
        für unbekannte Pfade den Statuscode 404.
        """
        pass

    def _handle_post_request(self, request):
        """
        Interne Methode: Bearbeitet POST /config. Liest den JSON-Body,
        übernimmt die neuen Einstellungen und speichert sie über den
        ConfigManager (siehe dort zum Thema Schreibschutz).

        Hinweise:
        - Der Body steht hinter der ersten Leerzeile ("\r\n\r\n") der Anfrage
          und ist so lang wie im Header "Content-Length" angegeben. Er kommt
          nicht immer in einem Stück an.
        - Ungültiges JSON oder unbekannte Felder mit 400 beantworten,
          nicht mit einem Absturz.
        """
        pass


# ===================================================================
# HAUPTPROGRAMM (Main Logic)
# ===================================================================

# 1. INITIALISIERUNG
#    - Status-LED initialisieren.
#    - ConfigManager erstellen und Konfiguration aus "settings.toml" laden.
#    - NetworkManager erstellen und mit den geladenen WLAN-Daten verbinden.
#      -> Währenddessen Status-LED blinken lassen.
#    - Sensor, MqttClient und WebServer mit den Konfigurationsdaten instanziieren.
#    - WebServer starten.

# 2. VERBINDUNGSAUFBAU
#    - Mit dem MqttClient zum Broker verbinden.
#    - Eine "ok"-Statusnachricht senden.
#    - Status-LED auf "dauerhaft an" setzen, um Betriebsbereitschaft zu signalisieren.

# 3. HAUPTSCHLEIFE (Endlosschleife)
#    - while True:
#        - MqttClient.loop() aufrufen, um die Verbindung zu halten.
#        - WebServer.poll() aufrufen, um Konfigurationsanfragen zu prüfen.
#
#        - Prüfen, ob das Sende-Intervall (reading_interval_seconds) abgelaufen ist.
#        - WENN ja:
#            a. Daten vom Sensor lesen (Sensor.read_data()).
#            b. WENN Daten gültig sind:
#               - Telemetrie über den MqttClient veröffentlichen.
#            c. WENN Daten ungültig sind:
#               - Fehler loggen oder anzeigen (z.B. durch Blinken der LED).
#               - Eine "error"-Statusnachricht senden.
#
#        - Fehlerbehandlung für getrennte WLAN- oder MQTT-Verbindungen implementieren
#          und versuchen, die Verbindung wiederherzustellen.
```

---

# Datei: `src/raspi_firmware/lib/toml.py`

```python
# lib/toml.py - minimaler TOML-Parser für CircuitPython
#
# Unterstützt einfache "schluessel = wert"-Zeilen mit Strings, Ganzzahlen,
# Kommazahlen und true/false sowie Kommentare (auch am Zeilenende).
# Nicht unterstützt: Tabellen/Sektionen ([abschnitt]) werden ignoriert,
# Listen, mehrzeilige Strings und Datumswerte.
#
# Achtung: dump()/dumps() schreibt nur "schluessel = wert"-Zeilen,
# Kommentare aus der Originaldatei gehen dabei verloren.


def _strip_comment(value):
    # Entfernt einen Kommentar (#) am Zeilenende, aber nicht innerhalb von Anführungszeichen
    quote = None
    for i, char in enumerate(value):
        if char in ('"', "'"):
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
        elif char == "#" and quote is None:
            return value[:i].strip()
    return value.strip()


def _parse_value(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    if value in ("true", "false"):
        return value == "true"
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def loads(s):
    data = {}
    for line in s.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("["):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = _parse_value(_strip_comment(value))
    return data


def load(f):
    return loads(f.read())


def dumps(data):
    out = []
    for k, v in data.items():
        if isinstance(v, bool):
            out.append(f"{k} = {'true' if v else 'false'}")
        elif isinstance(v, str):
            out.append(f'{k} = "{v}"')
        else:
            out.append(f"{k} = {v}")
    return "\n".join(out) + "\n"


def dump(data, f):
    f.write(dumps(data))
```

---

# Datei: `src/raspi_firmware/settings.toml`

```toml
# settings.toml

# ===================================================================
# IoT Environmental Monitoring - Konfigurationsdatei
# Diese Datei wird vom Raspberry Pi Pico W beim Start gelesen.
# Bitte die WLAN-Daten vor Ort anpassen.
# ===================================================================

# --- Geräteeinstellungen ---
# Eindeutiger Name für diesen Sensor, wird in den MQTT-Nachrichten verwendet.
# z.B. "prod-hall-3-vomp"
device_id = "yourmuesli-innsbruck-01"
names = "{nachname1-nachname2-nachname3}"

# Optionaler, menschenlesbarer Standort für das Web-Interface.
location = "Produktionshalle 1, Innsbruck"


# --- WLAN-Einstellungen ---
# SSID (Name) und Passwort des lokalen WLAN-Netzwerks.
# WICHTIG: Diese müssen vor Ort eingetragen werden!
wifi_ssid = "yourmuesli-produktion"
wifi_password = "SehrGeheimesPasswort123"


# --- MQTT Broker Einstellungen ---
# Die Adresse des zentralen Servers (Broker), an den die Daten gesendet werden.
broker_address = "158.180.44.197"
broker_port = 1883
mqtt_username = "bobm"
# Passwort wird in der Vorlesung bekanntgegeben.
mqtt_password = "In Vorlesung erfragen"

# Topics sind wie "Kanäle", auf denen Nachrichten gesendet werden.
# Struktur siehe docs/iot-specs/conventions.md
# Das Haupt-Topic für die Sensordaten (Temperatur, Luftfeuchtigkeit).
telemetry_topic = "iiot/group/{nachname1-nachname2-nachname3}/sensor/temperature/state"
# Das Topic für Statusmeldungen (z.B. "ok", "error", "offline").
status_topic = "iiot/group/{nachname1-nachname2-nachname3}/status"


# --- Sensor & Applikations-Einstellungen ---
# Das Intervall in Sekunden, in dem Daten gelesen und gesendet werden.
reading_interval_seconds = 60

# Der GPIO Pin des Raspberry Pi Pico, an dem das Datenkabel des
# DHT11-Sensors angeschlossen ist (z.B. GP22, siehe Materialien).
sensor_pin = 22
```

---

# Datei: `tests/requirements.txt`

```text
Flask==3.1.2
paho-mqtt==2.1.0
pytest==8.4.2
requests==2.32.5
```

---

# Datei: `tests/test_cloud.py`

```python
import importlib.util
import json
import os
from pathlib import Path


def load_cloud(tmp_path):
    os.environ["DATABASE_PATH"] = str(tmp_path / "test.sqlite3")
    os.environ["MQTT_HOST"] = "localhost"
    os.environ["DISABLE_MQTT"] = "1"
    spec = importlib.util.spec_from_file_location("cloud_app", Path(__file__).parents[1] / "src/cloud/app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Message:
    topic = "iiot/group/unterhuber-brachmann-reimeir-noessing/sensor/temperature/state"
    payload = json.dumps({"timestamp": "2026-11-02T10:00:00Z", "sensor_id": "yourmuesli-innsbruck-01", "value": 22.5, "unit": "°C", "status": "ok"}).encode()


def test_mqtt_reading_is_stored_and_exposed(tmp_path):
    cloud = load_cloud(tmp_path)
    cloud.on_message(None, None, Message())
    client = cloud.app.test_client()
    readings = client.get("/api/readings?group=unterhuber-brachmann-reimeir-noessing").get_json()
    assert readings[0]["value"] == 22.5
    assert client.get("/health").get_json() == {"status": "ok"}


def test_topic_parser_accepts_sensor_and_status_topics(tmp_path):
    cloud = load_cloud(tmp_path)
    assert cloud.parse_topic("iiot/group/team/sensor/temperature/state") == ("team", "temperature")
    assert cloud.parse_topic("iiot/group/team/status") == ("team", "status")
    assert cloud.parse_topic("invalid/topic") == (None, None)
```

---

# Datei: `tests/test_device_api.py`

```python
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
```
