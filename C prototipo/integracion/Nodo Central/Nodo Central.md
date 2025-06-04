## Nodo Central LoRa (ESP32 - Receptor, Control de Extractores y Publicador MQTT)

### Descripción General
El **Nodo Central LoRa** actúa como el **cerebro del sistema**, encargado de recibir los datos enviados por el sensor vía **LoRa**, procesarlos y ejecutar acciones sobre los **extractores** para la ventilación del área.  
Además, los datos se envían a una API a través del protocolo **MQTT**, permitiendo monitoreo remoto.  
También recibe comandos la aplicación móvil para activar/desactivar los extractores manualmente y en modo automatico hace su control
también por la app se puden  modificar los ubrales de acticvacion.


---

## **1. Componentes del Sistema**  

- **Hardware**:  
  - Microcontrolador **ESP32**  
  - Módulo **LoRa SX1276**  
  - Extractores de aire controlados mediante **PWM**  
  - Conexión **WiFi** para envío de datos  

- **Software**:  
  - Código en **C++** utilizando la plataforma **Arduino**  
  - Librerías: `WiFi.h`, `SPI.h`, `LoRa.h`, `PubSubClient.h`, `ControlVentilador.h`  
  - Comunicación **MQTT** con el broker `test.mosquitto.org`  
  - Aplicación móvil para el control manual  

| **Función** | **Descripción** |
|------------|----------------|
| `setup()` | Configura WiFi, MQTT y LoRa. Inicializa los pines de control de los extractores. |
| `loop()` | Mantiene la conectividad MQTT y ejecuta la lógica de procesamiento de datos recibidos vía LoRa. |
| `PROCESAR_LORA()` | Recibe y procesa datos de sensores vía LoRa, verificando umbrales y ejecutando acciones en extractores. |
| `CONTROL_AUTOMATICO_EXTRACTORES(valor_gas)` | Controla automáticamente los extractores según los niveles de gas detectados. |
| `CONFIGURAR_EXTRACTORES(potencia)` | Ajusta la velocidad de los extractores utilizando PWM. |
| `APAGAR_EXTRACTORES()` | Apaga todos los extractores para seguridad cuando el gas está en niveles bajos. |
| `CONECTAR_MQTT()` | Establece conexión con el broker MQTT y suscribe a temas relevantes. |
| `CALLBACK_MQTT_RECIBIDO(TEMA, MENSAJE)` | Procesa los comandos recibidos por MQTT desde la aplicación móvil. |
| `PUBLICAR_MQTT(cliente_mqtt, MQTT_TOPIC, MENSAJE)` | Publica datos del sensor y estado de los extractores en el broker MQTT. |


---

## **2. Arquitectura y Flujo de Datos**  

1. **Recepción LoRa**:  
   - Datos del sensor enviados en paquetes LoRa.  
   - Decodificación y procesamiento de los valores.  

2. **Procesamiento de datos**:  
   - Comprobación de umbrales de seguridad.  
   - Cálculo de ajuste de velocidad en extractores mediante PWM.  

3. **Control de extractores**:  
   - Activación automática según niveles de gas.  
   - Activación manual desde la aplicación móvil.  

4. **Publicación en MQTT**:  
   - Estado de sensores y extractores enviado a través de MQTT.  

5. **Recepción de comandos**:  
   - Modificación de parámetros desde la aplicación móvil vía MQTT.  

---

## **3. Funciones del Código**  

### **Inicialización**  

```c
void setup() {
  Serial.begin(9600);
  SPI.begin(SCK, MISO, MOSI, SS);
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("Error al iniciar LoRa");
    while (true);
  }

  WiFi.begin(ssid, password);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callbackMQTT);

  Serial.println("Nodo listo para operar");
}
```

---

### **Recepción de Datos LoRa**  
Esta función se encarga de leer los datos enviados por el sensor remoto y extraer la información relevante.  

```c
void recibirLoRa() {
  int packetSize = LoRa.parsePacket();
  if (packetSize > 0) {
    String mensaje = "";
    while (LoRa.available()) {
      mensaje += (char)LoRa.read();
    }
    procesarMensajeLoRa(mensaje);
  }
}
```

---

### **Procesamiento de Datos del Sensor**  

```c
void procesarMensajeLoRa(String mensaje) {
  if (mensaje.startsWith("GAS_DATA|")) {
    int p1 = mensaje.indexOf("PPM:") + 4;
    int p2 = mensaje.indexOf("|Ratio:");
    float ppm = mensaje.substring(p1, p2).toFloat();

    ultimaPPM = ppm;
    ultimoEstado = (ppm > umbralGas) ? "ALERTA" : "NORMAL";

    if (modoAutomatico) {
      if (ppm > umbralGas) {
        int pwm = map(ppm, umbralGas, 1000, 50, 100);
        extractor.establecerVelocidad(pwm);
      } else {
        extractor.apagar();
      }
    }

    publicarEstadoMQTT();
  }
}
```

---

### **Publicación en MQTT**  

```c
void publicarEstadoMQTT() {
  String payload = "{";
  payload += "\"ppm\":" + String(ultimaPPM, 1) + ",";
  payload += "\"estado\":\"" + ultimoEstado + "\"";
  payload += "}";
  client.publish(topic_envio, payload.c_str());
}
```

---
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


