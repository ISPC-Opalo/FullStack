#include <WiFi.h>
#include <SPI.h>
#include <LoRa.h>
#include <PubSubClient.h>
#include "ControlVentilador.h"

// Pines LoRa para ESP32
#define SCK     18
#define MISO    19
#define MOSI    23
#define SS      5
#define RST     14
#define DIO0    26

#define PIN_EXTRACTOR 27

// Configuración WiFi y MQTT
const char* ssid = "redmi";
const char* password = "123456789";
const char* mqtt_server = "test.mosquitto.org";
const char* topic_config = "gas/control";
const char* topic_envio = "gas/datos";

// Variables de estado
float umbralGas = 500.0;
bool modoAutomatico = false;
float ultimaPPM = 0;
float ultimaRatio = 0;
int ultimoRaw = 0;
String ultimoEstado = "NORMAL";

WiFiClient espClient;
PubSubClient client(espClient);
ControlVentilador extractor(PIN_EXTRACTOR, 100);

// Prototipos
void recibirLoRa();
void procesarMensajeLoRa(String mensaje);
void reconectarMQTT();
void callbackMQTT(char* topic, byte* payload, unsigned int length);
void publicarEstadoMQTT();

void setup() {
  Serial.begin(9600);
  delay(2000);
  Serial.println("🔄 Inicializando LoRa...");

  SPI.begin(SCK, MISO, MOSI, SS);
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("❌ Error al iniciar LoRa");
    while (true);
  }

  LoRa.setTxPower(20);
  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
 
  LoRa.setSyncWord(0x34); 

  Serial.println("✅ LoRa listo");

  Serial.println("🔄 Conectando WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
  
  delay(500); Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado");

  client.setServer(mqtt_server, 1883);
  client.setCallback(callbackMQTT);

  //extractor.inicializar();
  //extractor.configurarArranqueSuave(true, 100);
  //extractor.configurarTransicion(5, 50);
  //extractor.setPwmMax(255);

  Serial.println("✅ Receptor listo - Esperando mensajes...");
}

void loop() {
  // LoRa primero
  recibirLoRa();

  // 2. MQTT solo si está desconectado
  if (!client.connected()) reconectarMQTT();
  client.loop();

  // Ventilador
  extractor.actualizar();

  delay(5); // Cortito para no saturar
}

// ========== RECEPCIÓN LoRa ==========

void recibirLoRa() {
  int packetSize = LoRa.parsePacket();
  if (packetSize > 0) {
    Serial.println("Paquete recibido");

    String mensaje = "";
    while (LoRa.available()) {
      mensaje += (char)LoRa.read();
    }

    Serial.println("💬 Texto crudo recibido:");
    Serial.println("[" + mensaje + "]");
    Serial.println("📶 RSSI: " + String(LoRa.packetRssi()) + " dBm");
    Serial.println("📊 SNR: " + String(LoRa.packetSnr()) + " dB");
    Serial.println("──────────────────────────────");

    procesarMensajeLoRa(mensaje);
  }
}

// ========== PROCESAR MENSAJE ==========

void procesarMensajeLoRa(String mensaje) {
  if (mensaje.startsWith("GAS_DATA|")) {
    int p1 = mensaje.indexOf("PPM:") + 4;
    int p2 = mensaje.indexOf("|Ratio:");
    float ppm = mensaje.substring(p1, p2).toFloat();

    int p3 = mensaje.indexOf("Ratio:") + 6;
    int p4 = mensaje.indexOf("|Raw:");
    float ratio = mensaje.substring(p3, p4).toFloat();

    int p5 = mensaje.indexOf("Raw:") + 4;
    int p6 = mensaje.indexOf("|Status:");
    int raw = mensaje.substring(p5, p6).toInt();

    ultimaPPM = ppm;
    ultimaRatio = ratio;
    ultimoRaw = raw;
    ultimoEstado = (ppm > umbralGas) ? "ALERTA" : "NORMAL";

    Serial.println("✅ Datos procesados:");
    Serial.println("🔸 PPM: " + String(ppm));
    Serial.println("🔸 Ratio: " + String(ratio));
    Serial.println("🔸 Raw: " + String(raw));
    Serial.println("🔸 Estado: " + ultimoEstado);

    if (modoAutomatico) {
      if (ppm > umbralGas) {
        int pwm = map(ppm, umbralGas, 1000, 50, 100);
        pwm = constrain(pwm, 50, 100);
        extractor.establecerVelocidad(pwm);
        Serial.println("⚙️ Extractor ON (" + String(pwm) + "%)");
      } else {
        extractor.apagar();
        Serial.println("⚙️ Extractor OFF");
      }
    }

    publicarEstadoMQTT();
  } else {
    Serial.println(" Mensaje no reconocido: " + mensaje);
  }
}

// ========== MQTT ==========

void callbackMQTT(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.println("🔧 Comando MQTT: " + msg);

  if (msg == "extractor_on") {
    modoAutomatico = false;
    extractor.encender(80);
  } else if (msg == "extractor_off") {
    modoAutomatico = false;
    extractor.apagar();
  } else if (msg == "modo_auto_on") {
    modoAutomatico = true;
    Serial.println(" Modo automático activado");
  } else if (msg.startsWith("set_umbral:")) {
    float nuevo = msg.substring(11).toFloat();
    if (nuevo > 0 && nuevo < 5000) {
      umbralGas = nuevo;
      Serial.println(" Nuevo umbral: " + String(umbralGas));
    }
  }
}

void reconectarMQTT() {
  static unsigned long lastTry = 0;
  if (millis() - lastTry < 5000) return;
  lastTry = millis();

  Serial.print("🔌 Conectando a MQTT...");
  if (client.connect("esp32-receptor")) {
    Serial.println(" conectado.");
    client.subscribe(topic_config);
  } else {
    Serial.print(" fallo (rc=");
    Serial.print(client.state());
    Serial.println(")");
  }
}

void publicarEstadoMQTT() {
  String payload = "{";
  payload += "\"ppm\":" + String(ultimaPPM, 1) + ",";
  payload += "\"ratio\":" + String(ultimaRatio, 2) + ",";
  payload += "\"raw\":" + String(ultimoRaw) + ",";
  payload += "\"estado\":\"" + ultimoEstado + "\",";
  payload += "\"umbral\":" + String(umbralGas);
  payload += "}";
  client.publish(topic_envio, payload.c_str());
  Serial.println("📡 Estado enviado a MQTT");
}
