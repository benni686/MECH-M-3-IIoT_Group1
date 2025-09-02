# MQTT & Daten-Konventionen

## Topics
- Struktur: `iiot/group/{nachname1-nachname2-nachname3}/sensor/temperature/state`
- Nur Kleinbuchstaben und `/` als Trenner
- Beispiel: `iiot/group/mustermann-meier-schmidt/sensor/temperature/state`

## Payload
- Standardformat: JSON
- Zeitstempel immer in **UTC, ISO8601** (`2025-08-28T10:00:00Z`)
- Einheit als String (z. B. `"°C"`)
- Statuswerte: `ok`, `error`, `offline`

## Endpunkt

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
```json
{
  "sendInterval": 60,
  "deviceName": "sensor-node-01"
}