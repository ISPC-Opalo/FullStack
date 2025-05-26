#include <Arduino.h>
#include "ConfigStorage.h"
#include "WiFiManager.h"
#include "MqttManager.h"

#define WIFI_SSID  "Vitto"
#define WIFI_PASS  "vittorio10"
#define MQTT_HOST  "test.mosquitto.org"
#define MQTT_PORT  1883

ConfigStorage config("config");
WiFiManager   wifiMgr;
MqttManager   mqttMgr(config, wifiMgr);

void setup() {
  Serial.begin(115200);
    while (!Serial) {
    ; // espera a inicializar puerto serial
  }
  Serial.println("\n--- Iniciando Sistema ---");

  config.begin(false);
  Serial.println("[ConfigStorage] NVS inicializado");

  wifiMgr.begin(WIFI_SSID, WIFI_PASS);
  mqttMgr.begin(MQTT_HOST, MQTT_PORT);
}

void loop() {
  mqttMgr.loop();
}


