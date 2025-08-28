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