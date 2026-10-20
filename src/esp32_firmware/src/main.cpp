#include <Arduino.h>
#include <ArduinoJson.h>
#include <WebServer.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <Wire.h>
#include <time.h>

// Hardware from HygroMQTT:
// DHT20: SDA GPIO 8, SCL GPIO 9
// Analog hygrometers: GPIO 0 (A0) and GPIO 1
constexpr uint8_t DHT20_SDA_PIN = 8;
constexpr uint8_t DHT20_SCL_PIN = 9;
constexpr uint8_t HYGROMETER_1_PIN = 0;
constexpr uint8_t HYGROMETER_2_PIN = 1;
constexpr uint8_t DHT20_I2C_ADDR = 0x38;

// Credentials are injected from the ignored .env file by load_env.py.
constexpr char WIFI_SSID_VALUE[] = WIFI_SSID;
constexpr char WIFI_PASSWORD_VALUE[] = WIFI_PASSWORD;

// Set the group slug to the participating members' lowercase surnames.
constexpr char MQTT_GROUP[] = "hannes-unterhuber";
constexpr char DEVICE_ID[] = "yourmuesli-innsbruck-01";
constexpr char MQTT_HOST_VALUE[] = MQTT_BROKER_HOST;
constexpr bool MQTT_USE_TLS_VALUE =
    (MQTT_USE_TLS[0] == '1' || MQTT_USE_TLS[0] == 'y' || MQTT_USE_TLS[0] == 'Y' ||
     MQTT_USE_TLS[0] == 't' || MQTT_USE_TLS[0] == 'T');
constexpr uint16_t MQTT_PORT = MQTT_USE_TLS_VALUE ? 8883 : 1883;
constexpr char MQTT_USER_VALUE[] = MQTT_USER;
constexpr char MQTT_PASSWORD_VALUE[] = MQTT_PASSWORD;

constexpr unsigned long DEFAULT_INTERVAL_MS = 60000;
constexpr unsigned long WIFI_RETRY_MS = 10000;
constexpr unsigned long MQTT_RETRY_MS = 5000;
constexpr unsigned long DEBUG_STATUS_MS = 2000;
constexpr unsigned long DHT20_MEASUREMENT_DELAY_MS = 85;
constexpr int HYGRO_ADC_DRY = 3000;
constexpr int HYGRO_ADC_WET = 900;

WiFiClient wifiClient;
WiFiClientSecure secureClient;
PubSubClient mqttClient(wifiClient);
WebServer server(80);

String temperatureTopic;
String humidityTopic;
String hygrometer1Topic;
String hygrometer2Topic;
String statusTopic;
unsigned long readingIntervalMs = DEFAULT_INTERVAL_MS;
unsigned long lastReading = 0;
unsigned long lastWiFiAttempt = 0;
unsigned long lastMqttAttempt = 0;
unsigned long lastDebugStatus = 0;
bool dht20Detected = false;

String isoUtcNow() {
  time_t now = time(nullptr);
  struct tm utc {};
  gmtime_r(&now, &utc);
  char timestamp[25];
  strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", &utc);
  return String(timestamp);
}

void publishStatus(const char* status) {
  if (!mqttClient.connected()) {
    Serial.println("[MQTT] Status skipped: client is not connected");
    return;
  }

  JsonDocument document;
  document["status"] = status;
  document["timestamp"] = isoUtcNow();
  document["sensor_id"] = DEVICE_ID;
  String payload;
  serializeJson(document, payload);
  const bool published = mqttClient.publish(statusTopic.c_str(), payload.c_str(), true);
  Serial.printf("[MQTT] Status %s: %s -> %s\n",
                published ? "published" : "failed",
                statusTopic.c_str(), payload.c_str());
}

void publishReading(const char* topic, float value, const char* unit) {
  if (!mqttClient.connected()) {
    Serial.printf("[MQTT] Reading skipped: client is not connected (%s)\n", topic);
    return;
  }

  JsonDocument document;
  document["timestamp"] = isoUtcNow();
  document["sensor_id"] = DEVICE_ID;
  document["value"] = value;
  document["unit"] = unit;
  document["status"] = "ok";
  String payload;
  serializeJson(document, payload);

  const bool published = mqttClient.publish(topic, payload.c_str(), true);
  Serial.printf("[MQTT] Reading %s: %s -> %s\n",
                published ? "published" : "failed", topic, payload.c_str());
}

bool readDht20(float& humidity, float& temperature) {
  if (!dht20Detected) {
    return false;
  }

  Wire.beginTransmission(DHT20_I2C_ADDR);
  Wire.write(0xAC);
  Wire.write(0x33);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) {
    return false;
  }

  delay(DHT20_MEASUREMENT_DELAY_MS);
  if (Wire.requestFrom(DHT20_I2C_ADDR, static_cast<uint8_t>(7)) != 7) {
    return false;
  }

  uint8_t data[7];
  for (uint8_t& byte : data) {
    byte = Wire.read();
  }
  if ((data[0] & 0x80) != 0) {
    return false;
  }

  const uint32_t rawHumidity =
      (static_cast<uint32_t>(data[1]) << 12) |
      (static_cast<uint32_t>(data[2]) << 4) |
      (data[3] >> 4);
  const uint32_t rawTemperature =
      ((static_cast<uint32_t>(data[3]) & 0x0F) << 16) |
      (static_cast<uint32_t>(data[4]) << 8) |
      data[5];

  humidity = (rawHumidity / 1048576.0f) * 100.0f;
  temperature = (rawTemperature / 1048576.0f) * 200.0f - 50.0f;
  return humidity >= 0.0f && humidity <= 100.0f &&
         temperature >= -40.0f && temperature <= 85.0f;
}

float readHygrometer(uint8_t pin) {
  constexpr uint8_t sampleCount = 8;
  uint32_t sum = 0;
  for (uint8_t sample = 0; sample < sampleCount; ++sample) {
    sum += analogRead(pin);
    delay(2);
  }

  const int raw = static_cast<int>(sum / sampleCount);
  const float percentage =
      (static_cast<float>(HYGRO_ADC_DRY - raw) /
       static_cast<float>(HYGRO_ADC_DRY - HYGRO_ADC_WET)) * 100.0f;
  return constrain(percentage, 0.0f, 100.0f);
}

void publishSensorData() {
  if (!mqttClient.connected()) {
    Serial.println("[Sensor] Measurement skipped: MQTT is not connected");
    return;
  }

  float humidity = NAN;
  float temperature = NAN;
  const bool dhtOk = readDht20(humidity, temperature);
  const float hygrometer1 = readHygrometer(HYGROMETER_1_PIN);
  const float hygrometer2 = readHygrometer(HYGROMETER_2_PIN);

  Serial.printf("[Sensor] hygrometer 1: %.2f %% (GPIO %u), hygrometer 2: %.2f %% (GPIO %u)\n",
                hygrometer1, HYGROMETER_1_PIN, hygrometer2, HYGROMETER_2_PIN);
  if (dhtOk) {
    publishReading(temperatureTopic.c_str(), temperature, "°C");
    publishReading(humidityTopic.c_str(), humidity, "%");
    publishStatus("ok");
    Serial.printf("[Sensor] %.2f °C, %.2f %% RH, hygrometer 1: %.2f %%, hygrometer 2: %.2f %%\n",
                  temperature, humidity, hygrometer1, hygrometer2);
  } else {
    publishStatus("error");
    Serial.printf("[DHT20] Read failed (I2C address 0x%02X)\n", DHT20_I2C_ADDR);
  }
  publishReading(hygrometer1Topic.c_str(), hygrometer1, "%");
  publishReading(hygrometer2Topic.c_str(), hygrometer2, "%");
}

void handleGetConfig() {
  JsonDocument document;
  document["device_id"] = DEVICE_ID;
  document["reading_interval_seconds"] = readingIntervalMs / 1000;
  document["location"] = "Produktionshalle 1, Innsbruck";
  String response;
  serializeJson(document, response);
  server.send(200, "application/json", response);
}

void handlePostConfig() {
  JsonDocument document;
  const DeserializationError error = deserializeJson(document, server.arg("plain"));
  if (error) {
    server.send(400, "application/json", "{\"error\":\"invalid JSON\"}");
    return;
  }

  if (!document["reading_interval_seconds"].is<unsigned long>()) {
    server.send(400, "application/json",
                "{\"error\":\"reading_interval_seconds must be an integer\"}");
    return;
  }

  const unsigned long seconds = document["reading_interval_seconds"];
  if (seconds < 2 || seconds > 86400) {
    server.send(400, "application/json",
                "{\"error\":\"interval must be between 2 and 86400 seconds\"}");
    return;
  }

  readingIntervalMs = seconds * 1000UL;
  server.send(200, "application/json", "{\"status\":\"updated\"}");
}

void handleStatus() {
  JsonDocument document;
  document["device_id"] = DEVICE_ID;
  document["wifi_connected"] = WiFi.status() == WL_CONNECTED;
  document["mqtt_connected"] = mqttClient.connected();
  document["ip"] = WiFi.localIP().toString();
  String response;
  serializeJson(document, response);
  server.send(200, "application/json", response);
}

void handleNotFound() {
  server.send(404, "application/json", "{\"error\":\"not found\"}");
}

void setupRestApi() {
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/plain",
                "yourmuesli ESP32 sensor is running\n");
  });
  server.on("/config", HTTP_GET, handleGetConfig);
  server.on("/config", HTTP_POST, handlePostConfig);
  server.on("/status", HTTP_GET, handleStatus);
  server.onNotFound(handleNotFound);
  server.begin();
}

void connectWiFi() {
  Serial.printf("[WiFi] Connecting to SSID \"%s\"\n", WIFI_SSID_VALUE);
  WiFi.mode(WIFI_STA);
  if (!WiFi.setTxPower(WIFI_POWER_8_5dBm)) {
    Serial.println("[WiFi] Failed to set transmit power");
  }
  WiFi.setAutoReconnect(true);
  WiFi.disconnect();
  delay(100);
  WiFi.begin(WIFI_SSID_VALUE, WIFI_PASSWORD_VALUE);
}

void scanI2cBus() {
  Serial.printf("[I2C] Scanning SDA=%u, SCL=%u...\n", DHT20_SDA_PIN, DHT20_SCL_PIN);
  uint8_t found = 0;
  for (uint8_t address = 1; address < 127; ++address) {
    Wire.beginTransmission(address);
    const uint8_t error = Wire.endTransmission();
    if (error == 0) {
      Serial.printf("[I2C] Device found at 0x%02X%s\n", address,
                    address == DHT20_I2C_ADDR ? " (expected DHT20)" : "");
      ++found;
    }
  }
  if (found == 0) {
    Serial.println("[I2C] No devices found. Check power, GND, SDA/SCL and pull-ups.");
  }
}

const char* wifiStatusText(wl_status_t status) {
  switch (status) {
    case WL_CONNECTED: return "CONNECTED";
    case WL_NO_SSID_AVAIL: return "NO_SSID";
    case WL_CONNECT_FAILED: return "CONNECT_FAILED";
    case WL_CONNECTION_LOST: return "CONNECTION_LOST";
    case WL_DISCONNECTED: return "DISCONNECTED";
    default: return "OTHER";
  }
}

void printDebugStatus() {
  const wl_status_t status = WiFi.status();
  Serial.printf("[DEBUG] WiFi=%s (%d), RSSI=%d dBm, IP=%s, MQTT=%s, free heap=%u\n",
                wifiStatusText(status), status,
                status == WL_CONNECTED ? WiFi.RSSI() : 0,
                WiFi.localIP().toString().c_str(),
                mqttClient.connected() ? "CONNECTED" : "DISCONNECTED",
                ESP.getFreeHeap());
}

void connectMqtt() {
  if (WiFi.status() != WL_CONNECTED || mqttClient.connected()) {
    return;
  }

  const String clientId = "esp32c3-" + String(static_cast<uint32_t>(ESP.getEfuseMac()), HEX);
  Serial.printf("[MQTT] Connecting to %s as %s\n", MQTT_HOST_VALUE, clientId.c_str());
  if (mqttClient.connect(clientId.c_str(), MQTT_USER_VALUE, MQTT_PASSWORD_VALUE,
                         statusTopic.c_str(), 1, true, "{\"status\":\"offline\"}")) {
    Serial.println("[MQTT] Connected");
    publishStatus("ok");
    lastReading = millis() - readingIntervalMs;
  } else {
    Serial.printf("[MQTT] Connection failed, state=%d\n", mqttClient.state());
  }
}

void initializeDht20() {
  Wire.begin(DHT20_SDA_PIN, DHT20_SCL_PIN);
  Wire.setClock(100000);
  scanI2cBus();
  Wire.beginTransmission(DHT20_I2C_ADDR);
  dht20Detected = Wire.endTransmission() == 0;
  Serial.println(dht20Detected ? "[DHT20] Detected" : "[DHT20] Not detected");
}

void setup() {
  Serial.begin(115200);
  const unsigned long serialWaitStart = millis();
  while (!Serial && millis() - serialWaitStart < 5000) {
    delay(10);
  }
  delay(200);
  Serial.println("\n========== IIoT ESP32 SENSOR ==========");
  Serial.println("[BOOT] Debug logging enabled");
  Serial.println("[BOOT] This firmware supports a DHT20 over I2C, not a DHT11.");

  temperatureTopic = "iiot/group/" + String(MQTT_GROUP) +
                     "/sensor/temperature/state";
  humidityTopic = "iiot/group/" + String(MQTT_GROUP) +
                  "/sensor/humidity/state";
  hygrometer1Topic = "iiot/group/" + String(MQTT_GROUP) +
                     "/sensor/hygrometer-1/state";
  hygrometer2Topic = "iiot/group/" + String(MQTT_GROUP) +
                     "/sensor/hygrometer-2/state";
  statusTopic = "iiot/group/" + String(MQTT_GROUP) + "/status";
  Serial.printf("[MQTT] Temperature topic: %s\n", temperatureTopic.c_str());
  Serial.printf("[MQTT] Humidity topic: %s\n", humidityTopic.c_str());
  Serial.printf("[MQTT] Hygrometer 1 topic: %s\n", hygrometer1Topic.c_str());
  Serial.printf("[MQTT] Hygrometer 2 topic: %s\n", hygrometer2Topic.c_str());
  Serial.printf("[MQTT] Status topic: %s\n", statusTopic.c_str());

  analogReadResolution(12);
  analogSetPinAttenuation(HYGROMETER_1_PIN, ADC_11db);
  analogSetPinAttenuation(HYGROMETER_2_PIN, ADC_11db);
  initializeDht20();
  connectWiFi();
  lastWiFiAttempt = millis() - WIFI_RETRY_MS;
  lastDebugStatus = millis() - DEBUG_STATUS_MS;
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");

  if (MQTT_USE_TLS_VALUE) {
    // The EMQX Cloud certificate is validated by the broker hostname.
    secureClient.setInsecure();
    mqttClient.setClient(secureClient);
    Serial.println("[MQTT] TLS enabled");
  } else {
    mqttClient.setClient(wifiClient);
    Serial.println("[MQTT] TLS disabled (course-broker fallback)");
  }
  mqttClient.setServer(MQTT_HOST_VALUE, MQTT_PORT);
  setupRestApi();
}

void loop() {
  const unsigned long now = millis();

  if (WiFi.status() != WL_CONNECTED) {
    if (now - lastWiFiAttempt >= WIFI_RETRY_MS) {
      lastWiFiAttempt = now;
      connectWiFi();
    }
  } else if (!mqttClient.connected()) {
    if (now - lastMqttAttempt >= MQTT_RETRY_MS) {
      lastMqttAttempt = now;
      connectMqtt();
    }
  } else {
    mqttClient.loop();
  }

  if (now - lastReading >= readingIntervalMs) {
    lastReading = now;
    publishSensorData();
  }
  if (now - lastDebugStatus >= DEBUG_STATUS_MS) {
    lastDebugStatus = now;
    printDebugStatus();
  }

  server.handleClient();
  delay(10);
}
