

---

# **Documentación Técnica - Nodo Sensor LoRa (Arduino Uno)**  

## **1. Descripción General**  
El **Nodo Sensor LoRa** es un **Arduino Nano** equipado con un **sensor MQ** para medir la concentración de **CO₂** en el aire.  
Los datos se envían periódicamente vía **LoRa** al **Nodo Central ESP32**, utilizando una conexión **punto a punto** para el monitoreo de gases.

---

## **2. Funciones del Nodo Sensor**  

| **Función** | **Descripción** |
|------------|----------------|
| `setup()` | Inicializa el sensor MQ, configura LoRa y establece la comunicación con el Nodo Central. |
| `loop()` | Captura la lectura del sensor, la convierte en PPM y la transmite por LoRa. |
| `readRaw()` | Lee el valor **ADC** directamente del sensor MQ. |
| `readResistance()` | Calcula la **resistencia del sensor (Rs)** en función del voltaje. |
| `readRatio()` | Determina la **relación Rs/Ro**, comparando con aire limpio. |
| `readPPM()` | Convierte la lectura en **PPM de CO₂**, con calibración previa. |
| `sendLoRaMessage(mensaje)` | Envía los datos procesados al Nodo Central a través de LoRa. |
| `checkIncomingMessages()` | Revisa si hay comandos recibidos y los procesa. |

---

## **3. Flujo de Ejecución**  

1. **Inicialización:** Se configura **LoRa** y el **sensor MQ**, calibrándolo en aire limpio.  
2. **Lectura del sensor:** Se captura el valor **PPM de CO₂** con el sensor MQ.  
3. **Procesamiento de datos:** Se calcula la resistencia, ratio y valores de concentración de gas.  
4. **Formateo de datos:** Se genera un mensaje en **JSON** con los valores obtenidos.  
5. **Transmisión LoRa:** Se envía el mensaje al **Nodo Central ESP32**.  
6. **Recepción de comandos:** Se verifican mensajes recibidos y se ejecutan acciones según el comando.  

---

## **4. Código Principal**  

### **Inicialización del Nodo Sensor**  

```c
void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("=== NODO SENSOR NANO INICIANDO ===");

  // Configuración de LoRa
  LoRa.setPins(PIN_SS, PIN_RST, PIN_DIO0);
  if (!LoRa.begin(915E6)) {
    Serial.println("Error iniciando LoRa");
    while (1);
  }
  LoRa.setTxPower(20);
  LoRa.setSpreadingFactor(7);
  Serial.println("LoRa listo");

  // Calibración del sensor MQ
  Serial.println("Calibrando sensor MQ...");
  Ro = calibrateSensor();
  Serial.print("Calibración completa. Ro = ");
  Serial.print(Ro, 2);
  Serial.println(" kΩ");

  Serial.println("=== NODO SENSOR LISTO ===\n");
}
```

---

### **Lectura del Sensor MQ**  

```c
float readGasPPM() {
  float rs = calculateResistance(analogRead(GAS_PIN));
  float ratio = rs / Ro;
  
  // Ecuación para MQ-2
  float ppm = 574.25 * pow(ratio, -2.222);
  
  if (ppm < 0) ppm = 0;
  if (ppm > 10000) ppm = 10000;
  
  return ppm;
}
```

---

### **Envío de Datos por LoRa**  

```c
void sendLoRaMessage(String message) {
  LoRa.beginPacket();
  LoRa.print(message);
  LoRa.endPacket();

  Serial.print(" Enviado: ");
  Serial.println(message);
}
```

---

### **Recepción de Mensajes**  

```c
void checkIncomingMessages() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String receivedMsg = "";
    while (LoRa.available()) {
      receivedMsg += (char)LoRa.read();
    }

    Serial.print(" Recibido: ");
    Serial.println(receivedMsg);
    processMessage(receivedMsg);
  }
}
```

---

## **5. Configuración Regional - Argentina**  

| **Parámetro** | **Valor** |
|--------------|----------|
| **Región** | Argentina |
| **Denominación** | AU915 |
| **Banda ISM** | 915-928 MHz |
| **Regulado por** | ENACOM |
| **Restricción TX** | 400 ms (Opcional) |
| **Tamaño de carga útil (Payload)** | 11 a 242 bytes |
| **Spreading Factors** | SF7 a SF10 |
| **Velocidad de datos** | 0,976 kbps a 12,5 kbps |
| **Potencia máxima TX** | +30 dBm |

---

