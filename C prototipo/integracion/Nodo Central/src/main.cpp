#include <SPI.h>
#include <LoRa.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "ControlVentilador.h"
#include <time.h>

// ==============================
// CONFIGURACIÓN CONSTANTES
// ==============================

#define DEFAULT_SSID "DZS_5380"
#define DEFAULT_PASSWORD "dzsi123456789"
#define DEFAULT_UMB_GAS 500.0
#define DEFAULT_PWM_MAX 255

// Pin LoRa para ESP32
#define SCK    18
#define MISO   19
#define MOSI   23
#define SS     5
#define RST    14
#define DIO0   26

// Pin del extractor
#define PIN_EXTRACTOR 27


// ==============================
// CREDENCIALES MQTT
// ==============================
const char* mqtt_server = "telecomunicaciones.ddns.net";
const char* topic_config = "gas/control";
const char* topic_envio = "gas/datos";
const char* user_mqtt = "telecomunicaciones";
const char* pasword_mqtt = "cohorte*2024";

// ==============================
// VARIABLES
// ==============================
bool extraccionManualActiva = false;
unsigned long tiempoInicioManual = 0;
const unsigned long TIEMPO_MANUAL_MAX = 60000; // 1 minuto en milisegundos

char ssid[32] = DEFAULT_SSID;
char password[64] = DEFAULT_PASSWORD;

float umbralGas = DEFAULT_UMB_GAS;
bool modoAutomatico = true;
int pwmMax = DEFAULT_PWM_MAX;

WiFiClient espClient;
PubSubClient client(espClient);
ControlVentilador extractor(PIN_EXTRACTOR, 100);

const char* gatewayId = "esp32-central-88";
char timestamp[32];

float ultimaPPM = 0;
float ultimaRatio = 0;
int ultimoRaw = 0;
String ultimoEstado = "NORMAL";

// ==============================
//FUNCIONES
// ==============================

void callbackMQTT(char* topic, byte* payload, unsigned int length);
void reconectarMQTT();
void recibirLoRa();
void procesarMensajeLoRa(String mensaje);
void publicarEstadoMQTT();

void setup() {
  Serial.begin(9600);

  // Inicialización del ventilador
  extractor.inicializar();
  extractor.configurarArranqueSuave(true, 100);
  extractor.configurarTransicion(5, 50);

  // Conexión WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" WiFi conectado");

  // Configurar hora desde internet
  configTime(-3 * 3600, 0, "pool.ntp.org", "time.nist.gov");
  while (!time(nullptr)) delay(500);

  // Configuración MQTT
  client.setServer(mqtt_server, 2480);
  Serial.println(client.state());
  client.setCallback(callbackMQTT);

  // Inicializar LoRa
  LoRa.setPins(SS, RST, DIO0);
  if (!LoRa.begin(433000000L)) {
    Serial.println(" Error al iniciar LoRa");
    while (true);
  }
  Serial.println("LoRa listo");
}

void loop() {
  if (!client.connected()) reconectarMQTT();
  client.loop();

  recibirLoRa();
  extractor.actualizar();
}

void recibirLoRa() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String mensaje = "";
    while (LoRa.available()) mensaje += (char)LoRa.read();
    Serial.println("LoRa recibido: " + mensaje);
    procesarMensajeLoRa(mensaje);
  }
}

// ==============================
// FUNCIÓN  procesarMensajeLoRa
// ==============================
void procesarMensajeLoRa(String mensaje) {
  if (!mensaje.startsWith("GAS_DATA|")) return;

  // Parsear datos del mensaje LoRa
  ultimaPPM = mensaje.substring(mensaje.indexOf("PPM:") + 4, mensaje.indexOf("|Ratio:")).toFloat();
  ultimaRatio = mensaje.substring(mensaje.indexOf("Ratio:") + 6, mensaje.indexOf("|Raw:")).toFloat();
  ultimoRaw = mensaje.substring(mensaje.indexOf("Raw:") + 4, mensaje.indexOf("|Status:")).toInt();
  ultimoEstado = (ultimaPPM > umbralGas) ? "ALERTA" : "NORMAL";

  Serial.println("Datos sensor - PPM: " + String(ultimaPPM) + 
                 " | Ratio: " + String(ultimaRatio) + 
                 " | Raw: " + String(ultimoRaw) + 
                 " | Estado: " + ultimoEstado);

  // LÓGICA DE CONTROL
  if (modoAutomatico) {
    Serial.println("Modo automático activo");
    extraccionManualActiva = false; // Resetear modo manual
    
    // Control automático basado en PPM
    int pwm = 0;
    if (ultimaPPM > umbralGas) {
      // PPM sobre el umbral: calcular velocidad proporcional
      // hay que mapear desde umbral hasta umbral+500 → 50% a 100%
      float ppmExceso = ultimaPPM - umbralGas;
      pwm = map(ppmExceso, 0, 500, 50, 100);
      pwm = constrain(pwm, 50, 100);
      
      Serial.println("PPM SOBRE UMBRAL (" + String(umbralGas) + 
                     ") - Exceso: " + String(ppmExceso) + 
                     " → Velocidad: " + String(pwm) + "%");
    } else {
      //si no el  PPM esta bajo el umbral: apagar extractor
      pwm = 0;
      Serial.println(" PPM NORMAL (bajo umbral " + String(umbralGas) + 
                     ") → Extractor apagado");
    }
    
    extractor.establecerVelocidad(pwm);
    
  } else {
    Serial.println("Modo manual activo");
    
    // el modo manual: verificar tiempo de extracción activa
    if (extraccionManualActiva) {
      unsigned long tiempoTranscurrido = millis() - tiempoInicioManual;
      unsigned long tiempoRestante = TIEMPO_MANUAL_MAX - tiempoTranscurrido;
      
      Serial.println("Extracción manual activa - Faltan para el apagado: " + 
                     String(tiempoRestante / 1000) + "s");
      
      if (tiempoTranscurrido >= TIEMPO_MANUAL_MAX) {
        // tiempo de extracción alcanzado: vuelve  a modo automático
        Serial.println("Volviendo a automático");
        modoAutomatico = true;
        extraccionManualActiva = false;
        
        // Aplicar control automático inmediatamente
        int pwm = 0;
        if (ultimaPPM > umbralGas) {
          float ppmExceso = ultimaPPM - umbralGas;
          pwm = map(ppmExceso, 0, 500, 50, 100);
          pwm = constrain(pwm, 50, 100);
          Serial.println("control automático - PPM: " + String(ultimaPPM) + 
                         " → Velocidad: " + String(pwm) + "%");
        } else {
          Serial.println("control automático - PPM normal → Apagado");
        }
        extractor.establecerVelocidad(pwm);
      }
      // Si no hay timpo, hay que mantener estado actual
    } else {
      // Modo manual pero sin extracción activa
      Serial.println("Modo manual inactivo - Manteniendo estado actual");
    }
  }

  // Publicar estado actualizado
  publicarEstadoMQTT();
}
// ==============================
// FUNCIÓN publicarEstadoMQTT
// ==============================
void publicarEstadoMQTT() {
  if (!client.connected()) {
    Serial.println("no se puede publicar: MQTT no conectado");
    return;
  }

  time_t now = time(nullptr);
  struct tm* timeinfo = localtime(&now);
  strftime(timestamp, sizeof(timestamp), "%d/%m/%Y %H:%M:%S", timeinfo);

  String payload = "{";
  payload += "\"gatewayId\":\"" + String(gatewayId) + "\",";
  payload += "\"timestamp\":\"" + String(timestamp) + "\",";
  payload += "\"sensor\":{";
  payload += "\"ppm\":" + String(ultimaPPM, 1) + ",";
  payload += "\"ratio\":" + String(ultimaRatio, 2) + ",";
  payload += "\"raw\":" + String(ultimoRaw) + ",";
  payload += "\"estado\":\"" + ultimoEstado + "\",";
  payload += "\"umbral\":" + String(umbralGas);
  payload += "},";
  payload += "\"control\":{";
  payload += "\"automatico\":" + String(modoAutomatico ? "true" : "false") + ",";
  payload += "\"manual_activo\":" + String(extraccionManualActiva ? "true" : "false") + ",";
  payload += "\"encendido\":" + String(extractor.estaEncendido() ? "true" : "false") + ",";
  payload += "\"transicion\":" + String(extractor.estaEnTransicion() ? "true" : "false") + ",";
  payload += "\"velocidad\":" + String(extractor.obtenerVelocidadActual());
  payload += "},";
  payload += "\"actuador\":{";
  payload += "\"pin\":" + String(PIN_EXTRACTOR) + ","; // CORREGIDO: usar PIN_EXTRACTOR
  payload += "\"velocidad\":" + String(extractor.obtenerVelocidadActual()) + ",";
  payload += "\"objetivo\":" + String(extractor.obtenerVelocidadObjetivo()) + ",";
  payload += "\"pwm_max\":" + String(extractor.obtenerPwmMax()) + ",";  
  payload += "\"encendido\":" + String(extractor.estaEncendido() ? "true" : "false") + ",";
  payload += "\"transicion\":" + String(extractor.estaEnTransicion() ? "true" : "false");
  payload += "}";
  payload += "}"; 

  Serial.println("Payload length: " + String(payload.length()));
  Serial.println(" Enviando a MQTT:\n" + payload);

  client.setBufferSize(1024);
  bool ok = client.publish(topic_envio, payload.c_str());

  if (!ok) {
    Serial.println(" Error al publicar el mensaje MQTT.");
  }
}

// ==============================
// FUNCIÓN CORREGIDA: callbackMQTT
// ==============================
void callbackMQTT(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.println("MQTT recibido: " + msg);

  if (msg == "extractor_on") {
    Serial.println("Activando extractor manual");
    modoAutomatico = false;
    extraccionManualActiva = true;
    tiempoInicioManual = millis();
    extractor.encender(80);
    
  } else if (msg == "extractor_off") {
    Serial.println("Apagando extractor manual");
    modoAutomatico = false;
    extraccionManualActiva = false;
    extractor.apagar();
    
  } else if (msg == "modo_auto_on") {
    Serial.println("Activando modo automático");
    modoAutomatico = true;
    extraccionManualActiva = false;
    
  } else if (msg == "modo_auto_off") {
    Serial.println("Activando modo manual");
    modoAutomatico = false;
    extraccionManualActiva = false;
    // No cambiar estado del extractor, mantener como está
    
  } else if (msg.startsWith("set_umbral:")) {
    umbralGas = msg.substring(11).toFloat();
    Serial.println("Nuevo umbral: " + String(umbralGas));
  }
}

// ==============================
// Reconectar MQTT
// ==============================

void reconectarMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando a MQTT...");
    if (client.connect("esp32-central", user_mqtt, pasword_mqtt)) {
      Serial.println(client.state());
      Serial.println("conectado");
      client.subscribe(topic_config);
    } else {
      Serial.print("fallo (rc=");
      Serial.print(client.state());
      Serial.println("). Reintentando en 2s...");
      delay(2000);
    }
  }
}
