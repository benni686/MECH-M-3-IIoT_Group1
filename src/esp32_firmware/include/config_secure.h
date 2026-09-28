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
