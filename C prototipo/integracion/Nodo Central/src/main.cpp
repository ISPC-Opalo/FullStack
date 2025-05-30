#include <WiFi.h>
#include <SPI.h>
#include <LoRa.h>
#include <PubSubClient.h>
#include <Preferences.h>
#include "ControlVentilador.h"

// ==============================
// CONFIGURACIÓN WIFI y MQTT
// ==============================
const char* mqtt_server = "test.mosquitto.org";
const char* topic_config = "gas/control";
const char* topic_envio = "gas/datos";

char ssid[32]       = "SSID";
char password[64]   = "PASSWORD";

Preferences prefs;

// ==============================
// PINES Y VARIABLES
// ==============================
#define LORA_SS    5
#define LORA_RST   14
#define LORA_DIO0  2
#define PIN_EXTRACTOR 27

WiFiClient espClient;
PubSubClient client(espClient);
ControlVentilador extractor(PIN_EXTRACTOR, 100); // pin, PWM mínimo

float umbralGas = 500.0;
bool modoAutomatico = true;
float ultimaPPM = 0;
float ultimaRatio = 0;
int ultimoRaw = 0;
String ultimoEstado = "NORMAL";

// ==============================
// Prototipos
// ==============================
void cargarConfiguracion();
void guardarConfiguracion();
void callbackMQTT(char* topic, byte* payload, unsigned int length);
void reconectarMQTT();
void recibirLoRa();
void procesarMensajeLoRa(String mensaje);
void publicarEstadoMQTT();

// ==============================
// Funciones Preferences
// ==============================
void cargarConfiguracion() {
  prefs.begin("config", false);
  String s = prefs.getString("ssid", ssid);
  s.toCharArray(ssid, sizeof(ssid));
  String p = prefs.getString("pass", password);
  p.toCharArray(password, sizeof(password));
  umbralGas = prefs.getFloat("umbralGas", umbralGas);
  prefs.end();
}

void guardarConfiguracion() {
  prefs.begin("config", false);
  prefs.putString("ssid", ssid);
  prefs.putString("pass", password);
  prefs.putFloat("umbralGas", umbralGas);
  prefs.end();
}

// ==============================
// SETUP
// ==============================
void setup() {
  Serial.begin(115200);
  cargarConfiguracion();

  // Inicializar extractor
  extractor.inicializar();
  extractor.configurarArranqueSuave(true, 100);
  extractor.configurarTransicion(5, 50);

  // Conexión Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
  delay(3000);

  // MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callbackMQTT);

  // LoRa
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(915E6)) {
    Serial.println(" Error iniciando LoRa");
    while (1);
  }
  Serial.println(" LoRa listo");
}

// ==============================
// LOOP PRINCIPAL
// ==============================
void loop() {
  if (!client.connected()) reconectarMQTT();
  client.loop();

  recibirLoRa();
  extractor.actualizar();  // mantener transiciones PWM suaves
}

// ==============================
// LoRa
// ==============================
void recibirLoRa() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String msg;
    while (LoRa.available()) msg += (char)LoRa.read();
    Serial.println(" LoRa recibido: " + msg);
    procesarMensajeLoRa(msg);
  }
}

void procesarMensajeLoRa(String mensaje) {
  float ppm = 0;
  float ratio = 0;
  int raw = 0;
  String estado = "NORMAL";

  if (mensaje.startsWith("GAS_DATA|")) {
    int p1 = mensaje.indexOf("PPM:") + 4;
    int p2 = mensaje.indexOf("|Ratio:");
    ppm = mensaje.substring(p1, p2).toFloat();

    int p3 = mensaje.indexOf("Ratio:") + 6;
    int p4 = mensaje.indexOf("|Raw:");
    ratio = mensaje.substring(p3, p4).toFloat();

    int p5 = mensaje.indexOf("Raw:") + 4;
    int p6 = mensaje.indexOf("|Status:");
    raw = mensaje.substring(p5, p6).toInt();

    estado = (ppm > umbralGas) ? "ALERTA" : "NORMAL";

    if (modoAutomatico) {
      if (ppm > umbralGas) {
        int pwmPorcentaje = map(ppm, umbralGas, 1000, 50, 100);
        pwmPorcentaje = constrain(pwmPorcentaje, 50, 100);
        extractor.establecerVelocidad(pwmPorcentaje);
      } else {
        extractor.apagar();
      }
    }

    publicarEstadoMQTT();
  }
}

// ==============================
// MQTT
// ==============================
void callbackMQTT(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.println(" Comando MQTT: " + msg);

  if (msg == "extractor_on") {
    modoAutomatico = false;
    extractor.encender(80);
  } else if (msg == "extractor_off") {
    modoAutomatico = false;
    extractor.apagar();
  } else if (msg == "modo_auto_on") {
    modoAutomatico = true;
  } else if (msg.startsWith("set_umbral:")) {
    int nuevo = msg.substring(11).toInt();
    if (nuevo > 0 && nuevo < 5000) {
      umbralGas = nuevo;
      Serial.println(" Nuevo umbral: " + String(umbralGas));
      guardarConfiguracion();
    }
  } else if (msg.startsWith("set_ssid:")) {
    String nuevoSSID = msg.substring(9);
    nuevoSSID.toCharArray(ssid, sizeof(ssid));
    guardarConfiguracion();
    Serial.println("SSID guardado");
  } else if (msg.startsWith("set_pass:")) {
    String nuevoPass = msg.substring(9);
    nuevoPass.toCharArray(password, sizeof(password));
    guardarConfiguracion();
    Serial.println("Password guardada");
  } else if (msg.startsWith("set_velObj:")) {
    uint8_t v = msg.substring(11).toInt();
    extractor.establecerVelocidad(v);
    guardarConfiguracion();
    Serial.println("Velocidad Objetivo guardada");
  } else {
    Serial.println(" Comando desconocido: " + msg);
  }

}

void reconectarMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando a MQTT...");
    if (client.connect("esp32-central")) {
      Serial.println(" ok");
      client.subscribe("topic_config");
    } else {
      Serial.print("  (rc=");
      Serial.print(client.state());
      Serial.println(")");
      delay(2000);
    }
  }
}

// ==============================
// Publicar estado
// ==============================
void publicarEstadoMQTT() {
  String payload = "{";
  payload += "\"gatewayId\":\"esp32-central-001\",";
  payload += "\"timestamp\":" + String(millis()) + ",";
  payload += "\"sensor\":{";
  payload += "\"ppm\":" + String(ultimaPPM, 1) + ",";
  payload += "\"ratio\":" + String(ultimaRatio, 2) + ",";
  payload += "\"raw\":" + String(ultimoRaw) + ",";
  payload += "\"estado\":\"" + ultimoEstado + "\",";
  payload += "\"umbral\":" + String(umbralGas);
  payload += "},";
  payload += "\"control\":{";
  payload += "\"automatico\":" + String(modoAutomatico ? "true" : "false") + ",";
  payload += "\"encendido\":" + String(extractor.estaEncendido() ? "true" : "false") + ",";
  payload += "\"transicion\":" + String(extractor.estaEnTransicion() ? "true" : "false") + ",";
  payload += "\"velocidad\":" + String(extractor.obtenerVelocidadActual());
  payload += "},";
  payload += "\"estadoVentilador\":\"" + extractor.obtenerEstadoCompleto() + "\"";
  payload += "}";

  client.publish("topic_envio", payload.c_str());
  Serial.println(" MQTT publicado:");
  Serial.println(payload);
}
