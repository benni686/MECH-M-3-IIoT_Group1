# MQTT & Daten-Konventionen

## Topics
- Struktur: `building/{buildingId}/room/{roomId}/sensor/{type}/state`
- Nur Kleinbuchstaben und `/` als Trenner
- Beispiel: `building/A1/room/101/sensor/temperature/state`

## Payload
- Standardformat: JSON
- Zeitstempel immer in **UTC, ISO8601** (`2025-08-28T10:00:00Z`)
- Einheit als String (z. B. `"°C"`)
- Statuswerte: `ok`, `error`, `offline`


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