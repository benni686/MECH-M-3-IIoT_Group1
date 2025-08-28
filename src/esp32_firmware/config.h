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
const char* MQTT_BROKER_HOST = "your_mqtt_broker_host.com";
const int   MQTT_BROKER_PORT = 8883; // Standardport für MQTTS (TLS-verschlüsselt)
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