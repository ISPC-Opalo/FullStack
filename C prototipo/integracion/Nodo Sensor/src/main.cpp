#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>

//=======================================
// PINES LoRa para Arduino Nano
//=======================================
#define PIN_SS    10   // NSS
#define PIN_RST   9    // Reset
#define PIN_DIO0  2    // DIO0

//=======================================
// CONFIGURACIÓN SENSOR MQ (CO2/GAS)
//=======================================
#define GAS_PIN           A0    // Pin analógico para sensor MQ
#define VCC               5.0   // Voltaje Arduino Nano (5V)
#define RL_VALUE          10.0  // Resistencia de carga en kΩ
#define ADC_RESOLUTION    1024  // Resolución ADC Arduino (10 bits = 1024)
#define CLEAN_AIR_RATIO   9.8   // Rs/Ro en aire limpio (MQ-2)
#define CALIB_SAMPLES     50    // Muestras para calibración
#define CALIB_DELAY       500   // Delay entre muestras (ms)

//=======================================
// CONFIGURACIÓN
//=======================================
const unsigned long SEND_INTERVAL = 10000;  // Enviar datos cada 10 segundos
const float GAS_THRESHOLD = 500.0;           // Umbral de gas en PPM

//=======================================
// VARIABLES GLOBALES
//=======================================
float Ro = 10.0;  // Resistencia en aire limpio (kΩ)
unsigned long lastSendTime = 0;
float calibrateSensor();
float calculateResistance(int raw_adc);
float readGasPPM();
float readGasRatio();
void readAndSendGasData();
void sendLoRaMessage(String message);
void checkIncomingMessages();
void processMessage(String message);


//=======================================
// SETUP
//=======================================
void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println(F("=== NODO SENSOR NANO INICIANDO ==="));

  // Inicializar LoRa
  LoRa.setPins(PIN_SS, PIN_RST, PIN_DIO0);
  if (!LoRa.begin(915E6)) {
    Serial.println(F("Error iniciando LoRa"));
    while (1);
  }
  LoRa.setTxPower(20);
  LoRa.setSpreadingFactor(7);
  Serial.println(F("LoRa listo"));

  // Calibrar sensor MQ
  Serial.println(F("Calibrando sensor MQ..."));
  Serial.println(F("Tiene que estar el aire limpio"));
  delay(2000);
  
  Ro = calibrateSensor();
  Serial.print(F("Calibracion completa. Ro = "));
  Serial.print(Ro, 2);
  Serial.println(F(" kΩ"));
  
  Serial.println(F("=== NODO SENSOR LISTO ===\n"));
}

//=======================================
// LOOP PRINCIPAL
//=======================================
void loop() {
  // Enviar datos del sensor cada intervalo
  if (millis() - lastSendTime > SEND_INTERVAL) {
    readAndSendGasData();
    lastSendTime = millis();
  }
  
  // Verificar comandos recibidos
  checkIncomingMessages();
  
  delay(100);
}

//=======================================
// FUNCIONES DEL SENSOR MQ
//=======================================

float calibrateSensor() {
  float val = 0;
  
  // Tomar múltiples muestras para calibración
  for (int i = 0; i < CALIB_SAMPLES; i++) {
    val += calculateResistance(analogRead(GAS_PIN));
    delay(CALIB_DELAY);
  }
  
  val = val / CALIB_SAMPLES;                    // Promedio
  val = val / CLEAN_AIR_RATIO;                  // Rs/Ro = CLEAN_AIR_RATIO
  
  return val;
}

float calculateResistance(int raw_adc) {
  if (raw_adc == 0) return 0;
  
  float voltage = ((float)raw_adc / ADC_RESOLUTION) * VCC;
  float rs = (VCC - voltage) / voltage * RL_VALUE;
  
  return rs;
}

float readGasPPM() {
  float rs = calculateResistance(analogRead(GAS_PIN));
  float ratio = rs / Ro;
  
  // Ecuación para MQ-2 (aproximada)
  // PPM = A * (Rs/Ro)^B donde A=574.25, B=-2.222
  float ppm = 574.25 * pow(ratio, -2.222);
  
  // Limitar valores extremos
  if (ppm < 0) ppm = 0;
  if (ppm > 10000) ppm = 10000;
  
  return ppm;
}

float readGasRatio() {
  float rs = calculateResistance(analogRead(GAS_PIN));
  return rs / Ro;
}

//=======================================
// FUNCIONES PRINCIPALES
//=======================================

void readAndSendGasData() {
  Serial.println(F("--- Leyendo sensor de gas ---"));
  
  // Leer sensor MQ
  int rawValue = analogRead(GAS_PIN);
  float voltage = ((float)rawValue / ADC_RESOLUTION) * VCC;
  float rs = calculateResistance(rawValue);
  float ratio = readGasRatio();
  float ppm = readGasPPM();
  
  // Mostrar lecturas en Serial
  Serial.print(F("Raw: ")); Serial.print(rawValue);
  Serial.print(F(" | V: ")); Serial.print(voltage, 2);
  Serial.print(F("V | Rs: ")); Serial.print(rs, 2);
  Serial.print(F("kΩ | Ratio: ")); Serial.print(ratio, 2);
  Serial.print(F(" | PPM: ")); Serial.println(ppm, 1);
  
  // Evaluar umbral
  String status = (ppm > GAS_THRESHOLD) ? F("ALERTA") : F("NORMAL");
  
  // Crear mensaje
  String message = F("GAS_DATA|PPM:");
  message += String(ppm, 1);
  message += F("|Ratio:");
  message += String(ratio, 2);
  message += F("|Raw:");
  message += String(rawValue);
  message += F("|Status:");
  message += status;
  
  // Enviar por LoRa
  sendLoRaMessage(message);
  
  Serial.println(F("--- Datos enviados ---\n"));
}

void sendLoRaMessage(String message) {
  LoRa.beginPacket();
  LoRa.print(message);
  LoRa.endPacket();
  
  Serial.print(F(" Enviado: "));
  Serial.println(message);
}

void checkIncomingMessages() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String receivedMsg = "";
    while (LoRa.available()) {
      receivedMsg += (char)LoRa.read();
    }
    
    Serial.print(F(" Recibido: "));
    Serial.println(receivedMsg);
    processMessage(receivedMsg);
  }
}

void processMessage(String message) {
  message.trim();
  message.toUpperCase();
  
  if (message == "STATUS") {
    // Enviar datos inmediatamente
    Serial.println(F("Solicitud de estado recibida"));
    readAndSendGasData();
    
  } else if (message == "CALIBRATE") {
    // Re-calibrar sensor
    Serial.println(F("Re-calibrando sensor..."));
    Serial.println(F("Asegurate que este en aire limpio"));
    delay(3000);
    
    Ro = calibrateSensor();
    Serial.print(F("Nueva calibracion: Ro = "));
    Serial.print(Ro, 2);
    Serial.println(F(" kΩ"));
    
    String response = F("CALIBRATION_OK|Ro:");
    response += String(Ro, 2);
    sendLoRaMessage(response);
    
  } else if (message.startsWith("THRESHOLD:")) {
    // Cambiar umbral (ejemplo: THRESHOLD:600)
    float newThreshold = message.substring(10).toFloat();
    if (newThreshold > 0 && newThreshold < 5000) {
      Serial.print(F("Solicitud cambio umbral a: "));
      Serial.println(newThreshold);
      
      String response = F("THRESHOLD_ACK|");
      response += String(newThreshold);
      sendLoRaMessage(response);
    } else {
      sendLoRaMessage(F("THRESHOLD_ERROR|INVALID_VALUE"));
    }
    
  } else if (message == "INFO") {
    // Enviar información del nodo
    String info = F("NODE_INFO|TYPE:SENSOR|MCU:NANO|Ro:");
    info += String(Ro, 2);
    info += F("|THRESHOLD:");
    info += String(GAS_THRESHOLD);
    sendLoRaMessage(info);
    
  } else if (message == "RESET") {
    Serial.println(F("Reiniciando por comando remoto..."));
    sendLoRaMessage(F("RESET_ACK"));
    delay(1000);
  
    asm volatile ("  jmp 0");  // Reset por software
    
  } else {
    Serial.print(F("Comando no reconocido: "));
    Serial.println(message);
    sendLoRaMessage(F("ERROR|UNKNOWN_COMMAND"));
  }
}