#pragma once
#include <AsyncMqttClient.h>
#include <ArduinoJson.h>
#include <Arduino.h>
#include "ConfigStorage.h"
#include "WiFiManager.h"

class MqttManager {
public:
  MqttManager(ConfigStorage& cfg, WiFiManager& wifi)
    : _cfg(cfg), _wifi(wifi), _lastPublish(0) {}

  void begin(const char* host, uint16_t port) {
    _mqtt.onConnect([this](bool sessionPresent) {
      Serial.println("[MQTT] Connected to broker");
      _mqtt.subscribe("config/prueba/vitto2", 0);
      Serial.println("[MQTT] Subscribed to config/prueba/vitto2");
    });
    _mqtt.onMessage([this](char* topic, char* payload, AsyncMqttClientMessageProperties props, size_t len, size_t index, size_t total) {
      Serial.printf("[MQTT] Message arrived on topic %s: %.*s\n", topic, (int)len, payload);
      DynamicJsonDocument doc(64);
      if (deserializeJson(doc, payload, len) == DeserializationError::Ok) {
        if (doc.containsKey("interval")) {
          int secs = doc["interval"].as<int>();
          _cfg.putInt("interval_s", secs);
          Serial.printf("[Config] interval_s updated to %d s\n", secs);
        }
      } else {
        Serial.println("[MQTT] JSON parse error");
      }
    });

    _mqtt.setServer(host, port);
    _wifi.onConnect([this]() {
      Serial.println("[MQTT] Attempting to connect to broker...");
      _mqtt.connect();
    });
  }

  void loop() {
    if (!_wifi.isConnected() || !_mqtt.connected()) return;

    unsigned long now = millis();
    int interval = _cfg.getInt("interval_s", 3);
    if (now - _lastPublish >= (unsigned long)interval * 1000UL) {
      const char* msg = "hola";
      _mqtt.publish("prueba/vitto", 0, false, msg);
      Serial.printf("[Publish] %s at %lu ms (interval %d s)\n", msg, now, interval);
      _lastPublish = now;
    }
  }

private:
  ConfigStorage& _cfg;
  WiFiManager& _wifi;
  AsyncMqttClient _mqtt;
  unsigned long _lastPublish;
};
