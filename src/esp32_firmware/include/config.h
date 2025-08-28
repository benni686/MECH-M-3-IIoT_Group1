#ifndef CONFIG_H
#define CONFIG_H

// Dieser Header ist für große, statische Daten wie Zertifikate gedacht.

const int MQTT_BROKER_PORT = 8883;

const char* MQTT_BROKER_CA_CERT = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
...
-----END CERTIFICATE-----
)EOF";

#endif