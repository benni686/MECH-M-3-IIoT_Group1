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
extern WiFiClientSecure espClient;
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

        char macStr[18];
        sprintf(macStr, "%02X%02X%02X", WiFi.macAddress()[3], WiFi.macAddress()[4], WiFi.macAddress()[5]);
        sensorId = String(MQTT_CLIENT_ID_PREFIX) + String(macStr);

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
            espClient.setCACert(MQTT_BROKER_CA_CERT); // Zertifikat aus config_secure.h
            mqttClient.setServer(MQTT_BROKER_HOST, MQTT_SECURE_PORT); // Sicherer Port
        } else {
            Serial.println("Setting up insecure MQTT connection. NO CERTIFICATE WILL BE USED.");
            mqttClient.setServer(MQTT_BROKER_HOST, MQTT_INSECURE_PORT); // Unsicherer Port
        }
        
        mqttClient.setCallback(mqttCallback);
    }

    void reconnectMqtt() {
        while (!mqttClient.connected()) {
            Serial.print("Attempting MQTT connection...");
            if (mqttClient.connect(sensorId.c_str())) {
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