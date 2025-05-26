## Nodo Central LoRa (ESP32 - Receptor, Control de Extractores y Publicador MQTT)

### Descripción General
El **Nodo Central LoRa** actúa como el **cerebro del sistema**, encargado de recibir los datos enviados por el sensor vía **LoRa**, procesarlos y ejecutar acciones sobre los **extractores** para la ventilación del área.  
Además, los datos se envían a una API a través del protocolo **MQTT**, permitiendo monitoreo remoto.  
También recibe comandos desde la API y la aplicación móvil para activar/desactivar los extractores manualmente.

### Funciones del Nodo Central
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

### Flujo de Ejecución
1. **Inicialización:** Se establece la conectividad WiFi, MQTT y LoRa.
2. **Recepción de datos:** Se recibe información de los sensores vía LoRa.
3. **Procesamiento de información:** Se comparan los valores con los umbrales definidos.
4. **Activación de extractores:** Se ajusta la velocidad de ventilación según los niveles de gas.
5. **Publicación de datos:** Se envían los registros a la API vía MQTT.
6. **Recepción de comandos:** Se procesan órdenes de la aplicación móvil para activar/desactivar extractores manualmente.