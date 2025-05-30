#pragma once
#include <WiFi.h>
#include <functional>

class WiFiManager {
public:
  using EventCallback = std::function<void()>;

  WiFiManager() : _connected(false) {}

  void begin(const char* ssid, const char* pass) {
    WiFi.onEvent([this](WiFiEvent_t, WiFiEventInfo_t) {
      _connected = true;
      if (_onConnect) _onConnect();
      Serial.println("[WiFi] Connected, IP: " + WiFi.localIP().toString());
    }, ARDUINO_EVENT_WIFI_STA_GOT_IP);

    WiFi.onEvent([this](WiFiEvent_t, WiFiEventInfo_t) {
      _connected = false;
      Serial.println("[WiFi] Disconnected");
    }, ARDUINO_EVENT_WIFI_STA_DISCONNECTED);

    WiFi.begin(ssid, pass);
    Serial.printf("[WiFi] Connecting to %s ...\n", ssid);
  }

  bool isConnected() const { return _connected; }
  void onConnect(EventCallback cb) { _onConnect = cb; }

private:
  bool _connected;
  EventCallback _onConnect;
};
