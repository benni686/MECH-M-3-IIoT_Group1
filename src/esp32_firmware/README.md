# IIoT-Sensor – ESP32-C3, DHT20 und Hygrometer

Die Firmware setzt die Vorgaben aus `MECH-M-3-IIoT` um und verwendet die
Hardware aus diesem Projekt: einen DHT20 über I²C sowie zwei analoge
Hygrometer-Sensoren.

> Das MQTT-Passwort des Kurs-Brokers wird laut Aufgabenstellung in der
> Vorlesung bekanntgegeben. Vor dem Upload muss `MQTT_PASSWORD` in
> `src/main.cpp` ersetzt werden. Der Gruppenname `MQTT_GROUP` muss ebenfalls
> an die tatsächlichen Nachnamen der Gruppe angepasst werden.

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
3. `MQTT_GROUP` in `src/main.cpp` anpassen.
4. ESP32-C3 über USB anschließen.
5. Mit `pio run -t upload` flashen.
6. Die serielle Ausgabe mit `pio device monitor --baud 115200` öffnen.

Die lokale `.env` ist in `.gitignore` ausgeschlossen und enthält das WLAN- sowie
das MQTT-Passwort.

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
