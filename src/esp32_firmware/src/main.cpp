#include <Arduino.h>
#include "sensors/my_sensor.h" // Unser konkreter Sensor
#include "Sensor.h"           // Die Sensor-Basisklasse

// ----- Globale Definitionen -----
// Diese Objekte werden von der Sensor-Klasse als 'extern' erwartet.
WiFiClientSecure espClient;
PubSubClient mqttClient(espClient);
WebServer server(80);
Preferences preferences;

// ----- Sensor-Instanz erstellen -----
// Hier wird der Sensor konfiguriert.
// Parameter: Ort, Beschreibung, true/false für sichere/unsichere MQTT-Verbindung
MyTempSensor mySensor("Wohnzimmer", "Temperatur und Luftfeuchte", true);


void setup() {
    Serial.begin(115200);
    delay(1000); // Gibt der seriellen Konsole Zeit, sich zu verbinden

    // Das WIFI_SSID, WIFI_PASSWORD und MQTT_BROKER_HOST Makro wird
    // zur Kompilierzeit von platformio.ini hier eingesetzt.
    mySensor.setupWifiAndMqtt();
    mySensor.setupRestApi();

    Serial.println("Setup complete. Starting main loop...");
}

void loop() {
    mySensor.loop();
    mySensor.handleRestApi();
}


// ----- Implementierung der restlichen Sensor-Methoden -----
// Da sie im Header nur deklariert wurden, müssen sie hier implementiert werden.
// Alternativ könnte man eine Sensor.cpp-Datei erstellen.

void Sensor::publishSensorData(float value) {
    StaticJsonDocument<256> doc;
    doc["sensorId"] = sensorId;
    doc["sensorName"] = sensorName;
    doc["timestamp"] = millis();
    buildSensorDataJson(doc, value); // Ruft die Methode der abgeleiteten Klasse auf
    String output;
    serializeJson(doc, output);
    if (mqttClient.publish(mqttTopicData.c_str(), output.c_str())) {
        Serial.println("Published data: " + output);
    } else {
        Serial.println("Failed to publish data.");
    }
}

void Sensor::publishMetadata() {
    StaticJsonDocument<512> doc;
    doc["sensorId"] = sensorId;
    doc["sensorName"] = sensorName;
    doc["type"] = metadata.type;
    doc["unit"] = metadata.unit;
    // ... (Rest der Metadaten)
    String output;
    serializeJson(doc, output);
    if (mqttClient.publish(mqttTopicMeta.c_str(), output.c_str(), true)) {
        Serial.println("Published metadata (retained): " + output);
    } else {
        Serial.println("Failed to publish metadata.");
    }
}

void Sensor::setupRestApi() { /* ... Implementierung der REST API ... */ }
void Sensor::handleRestApi() { server.handleClient(); }
void Sensor::handleGetSettings() { /* ... */ }
void Sensor::handlePostSettings() { /* ... */ }
void Sensor::mqttCallback(char* topic, byte* payload, unsigned int length) { /* ... */ }