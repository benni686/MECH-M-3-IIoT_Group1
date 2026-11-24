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
- ein über TOML-Profile konfiguriertes WLAN
- den Kurs-MQTT-Broker gemäß `docs/iot-specs/conventions.md`

`settings.toml` enthält ausschließlich versionierbare Projekt- und Kurswerte.
Geheimnisse und der optionale private Broker stehen in der ignorierten
`settings.local.toml`. Einmalig einrichten:

```bash
cp settings.local.example.toml settings.local.toml
# settings.local.toml ausfüllen
```

ESP32 und Cloud-Stack lesen dieselben Dateien. Der Build wird aus dem
Firmware-Ordner gestartet:

```bash
pio run
pio run -t upload
pio device monitor --baud 115200
```

Die Firmware bietet außerdem `GET /config`, `POST /config` und `GET /status`
über die lokale IP-Adresse des ESP32 an.

## Cloud: Collector, Streamlit und Grafana

Im Repository-Stamm starten:

```bash
docker compose up --build
```

Es laufen drei dauerhafte Dienste und zwei kurze Initialisierungsdienste auf einer
gemeinsamen SQLite-Datenbank (Volume `iiot-data`):

| Dienst | Aufgabe | Adresse |
|---|---|---|
| `config-init` | validiert TOML und stellt Grafana sein Passwort dateibasiert bereit | - |
| `grafana-password-sync` | gleicht das Adminpasswort auch bei bestehenden Grafana-Volumes ab | - |
| `collector` | abonniert `iiot/group/#` und speichert alle Messwerte, auch wenn kein Dashboard offen ist | - |
| `dashboard` | Streamlit-Dashboard | http://localhost:8080 |
| `grafana` | Grafana-Dashboard "IIoT Sensor-Dashboard" (anonym lesbar; Admin-Daten aus TOML) | http://localhost:3000 |

Beide Dashboards bieten Auswahl von Gruppe, Sensoren und Zeitraum, aktuelle Werte,
Zeitverläufe je Einheit, Gerätestatus, letzte Verbindung und Rohdaten. Streamlit
zeigt zusätzlich Sensoranzahl sowie Minimum, Mittelwert und Maximum. Grafana nutzt das Plugin
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
docker compose ps                  # collector und dashboard sollten "healthy" sein
docker compose down                # Container stoppen, Daten behalten
```

`docker compose down -v` löscht auch die Messdaten und darf nur bewusst verwendet werden.

## Konfigurations- und Secret-Konzept

- `settings.toml` wird committed: Gruppen-Slug, Gerätewerte und Kurs-Broker ohne Passwort.
- `settings.local.example.toml` wird committed: dokumentierte Vorlage ohne echte Zugangsdaten.
- `settings.local.toml` wird ignoriert: WLAN-Passwörter, Kurs-Passwort, privater Broker und Grafana-Passwort.
- Zur Umschaltung auf den privaten Broker in `settings.local.toml` unter `[broker]`
  `active = "private"` setzen. Die Zugangsdaten bleiben lokal.

Alte lokale `.env`-Dateien können einmalig migriert werden:

```bash
python scripts/migrate_env_to_toml.py
```

## Dokumentation lokal bauen

```bash
pdm install
pdm run quarto preview
```

Bei jedem Push auf `main` wird die Website automatisch per GitHub Action gebaut und veröffentlicht (`.github/workflows/publish.yml`).
