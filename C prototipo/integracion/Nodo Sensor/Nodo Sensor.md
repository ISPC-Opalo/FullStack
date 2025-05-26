##  **1. Nodo Sensor LoRa (Arduino Nano - Transmisor de Datos de Gases)**

###  **Descripción General**
El **Nodo Sensor** es un **Arduino Nano** que emplea un sensor **MQ** para medir la concentración de **CO₂** en el aire.  
Los datos son enviados periódicamente vía **LoRa** a **ESP32**, utilizando una conexión **punto a punto**.

### ** Funciones del Nodo Sensor**
| **Función** | **Descripción** |
|------------|----------------|
| `setup()` | Inicializa el sensor MQ, configura LoRa y establece la comunicación con el Nodo Central. |
| `loop()` | Captura la lectura del sensor, la convierte en PPM y la transmite por LoRa. |
| `readRaw()` | Lee el valor **ADC** directamente del sensor MQ. |
| `readResistance()` | Calcula la **resistencia del sensor (Rs)** en función del voltaje. |
| `readRatio()` | Determina la **relación Rs/Ro**, comparando con aire limpio. |
| `readPPM()` | Convierte la lectura en **PPM de CO₂**, con calibración previa. |

### ** Flujo de Ejecución**
1. **Inicialización:** Se configura LoRa y el sensor MQ, calibrándolo en aire limpio.
2. **Lectura del sensor:** Se captura el valor **PPM de CO₂**.
3. **Formateo de datos:** Se genera un mensaje en **JSON**.
4. **Transmisión LoRa:** Se envía el mensaje al **Nodo Central** (ESP32).
5. **Espera de intervalo:** Se mantiene un lapso antes de la siguiente medición.

---

