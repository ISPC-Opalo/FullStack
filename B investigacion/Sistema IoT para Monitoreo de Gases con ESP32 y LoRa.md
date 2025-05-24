# **Sistema IoT para Monitoreo de Gases con ESP32 y LoRa**

##  Introducción

Este sistema de monitoreo de calidad del aire utiliza **ESP32** como unidades de procesamiento y comunicación, empleando **LoRa** para transmisión de datos y **MQTT** para integración con una API externa.  
Está compuesto por **dos nodos** con funciones específicas:

1. **Nodo Sensor LoRa (Transmisor de Datos de Gases)**  
2. **Nodo Central LoRa (Receptor LoRa, Publicador MQTT, Control de Extractores)**  

Cada nodo se comunica de manera eficiente y opera con funciones diseñadas para garantizar estabilidad y escalabilidad del sistema.

---

##  **1. Nodo Sensor LoRa (ESP32 - Transmisor de Datos de Gases)**

###  Descripción General
El **Nodo Sensor LoRa** se encarga de detectar la concentración de gases utilizando un sensor específico y transmitir los datos de forma inalámbrica mediante **LoRa** al **Nodo Central**.  
Esto permite realizar monitoreo remoto en áreas donde la conectividad WiFi o Ethernet es limitada.

###  Funciones del Nodo Sensor
| **Función** | **Descripción** |
|------------|----------------|
| `setup()` | Inicializa el módulo LoRa, el sensor de gas y la configuración del ESP32. Establece parámetros de comunicación. |
| `loop()` | Se ejecuta constantemente, leyendo datos del sensor, formateándolos y enviándolos por LoRa. |
| `LEER_VALOR_SENSOR_GAS()` | Obtiene la lectura del sensor de gas y la convierte en unidades PPM (Partes por Millón). |
| `CREAR_OBJETO_JSON(mensaje)` | Crea un objeto JSON con los datos del sensor para enviar. |
| `CONVERTIR_A_CADENA_JSON_PLANA(mensaje)` | Convierte el objeto JSON en una cadena lista para transmitir. |
| `LORA_BEGIN_PACKET()` | Inicia el proceso de envío de datos por LoRa. |
| `LORA_PRINT(mensaje_json_str)` | Envía el mensaje por LoRa en formato JSON. |
| `LORA_END_PACKET(confirmación)` | Finaliza la transmisión. La confirmación es opcional. |
| `ESPERAR(intervalo)` | Pausa la ejecución del código por un intervalo determinado antes de realizar una nueva medición. |

### Flujo de Ejecución
1. **Inicialización:** Se configura el ESP32, el módulo LoRa y el sensor de gas.
2. **Lectura del sensor:** Se captura la concentración de gas.
3. **Formateo de datos:** Se crea un mensaje en formato JSON.
4. **Transmisión LoRa:** El mensaje JSON se envía al Nodo Central.
5. **Espera de intervalo:** Se mantiene un lapso antes de la siguiente medición.

---

##  **2. Nodo Central LoRa (ESP32 - Receptor, Control de Extractores y Publicador MQTT)**

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

---

##  Interacción entre Nodos
### Flujo de Datos del Sistema
1. **Nodo Sensor LoRa** obtiene la concentración de gas y envía un mensaje **LoRa** en formato JSON.
2. **Nodo Central LoRa** recibe los datos y decide si activar, ajustar o apagar los extractores según los umbrales.
3. **Nodo Central LoRa** publica los datos en **MQTT**, permitiendo que la API almacene y visualice los valores en tiempo real.
4. **Aplicación móvil** envía comandos MQTT para control manual de extractores, los cuales son procesados por el **Nodo Central**.

---

##  Seguridad y Robustez
- **LoRa:** Garantiza comunicación **inalámbrica** de largo alcance con bajo consumo energético.
- **MQTT:** Permite integración con una API y control remoto mediante **mensajería en tiempo real**.
- **WiFi Reconectable:** Si la conexión WiFi se pierde, el sistema intenta reconectar automáticamente.
- **Control Manual de Extractores:** Los usuarios pueden activar/desactivar los extractores manualmente mediante MQTT.
- **Gestión de Errores:** Si MQTT no está disponible, los datos pueden almacenarse en memoria temporalmente hasta la reconexión.




ESP32 "Nodo Sensor LoRa",


INICIO

Configuración Inicial
FUNCION setup():  
    INICIALIZAR Serial  
    INICIALIZAR ModuloLoRa(frecuencia=868MHz, factor_esparcimiento=SF7)   
    CONFIGURAR ModuloLoRa(modo="transmisor")  
    ESTABLECER ID_DISPOSITIVO_SENSOR("SENSOR_GAS_01")  
    CONECTAR SensorGas(pin_analogico/digital)  
    INICIALIZAR SensorGas()  

Bucle Principal 
FUNCION loop():  
    Leer datos del sensor de gas  
    VALOR_GAS = LEER_VALOR_SENSOR_GAS()   

    Preparar el mensaje para enviar por LoRa  
    mensaje = CREAR_OBJETO_JSON()  
    mensaje.id_dispositivo = ID_DISPOSITIVO_SENSOR  
    mensaje.tipo_dato = "concentracion_gas"  
    mensaje.valor = VALOR_GAS  
    mensaje.timestamp = OBTENER_TIEMPO_ACTUAL()  

    mensaje_json_str = CONVERTIR_A_CADENA_JSON_PLANA(mensaje)   

    Enviar el mensaje por LoRa  
    IMPRIMIR "Enviando por LoRa: " + mensaje_json_str  
    LO_RA_BEGIN_PACKET()  
    LO_RA_PRINT(mensaje_json_str)  
    LO_RA_END_PACKET(confirmacion=true)  
    IMPRIMIR "Mensaje LoRa enviado."  

    Esperar un intervalo antes de la siguiente lectura  
    ESPERAR(5000)  


Funciones Auxiliares  
FUNCION LEER_VALOR_SENSOR_GAS():  
    valor_raw = LEER_PIN_ANALOGICO(PIN_SENSOR_GAS)  
    valor_calibrado = CALIBRAR_VALOR_A_PPM(valor_raw)  
    RETORNAR valor_calibrado  

FIN  

ESP32 "Nodo Central LoRa"  

INICIO  

Variables Globales  
MQTT_CLIENT cliente_mqtt  
STRING MQTT_BROKER_IP = "IP_DE_TU_BROKER_MQTT"  
INT MQTT_BROKER_PORT = 1883  
STRING MQTT_TOPIC_SENSORES = "sensores/data"  
STRING MQTT_TOPIC_COMANDOS_EXTRACTORES = "acciones/comandos_extractores"  
STRING MQTT_TOPIC_ESTADO_EXTRACTORES = "acciones/estado_extractores"  
STRING WIFI_SSID = "Tu_SSID_WiFi"  
STRING WIFI_PASSWORD = "Tu_Contrasena_WiFi"  

// Pines de Control de Extractores  
PIN_CONTROL_EXTRACTOR_1 = 23  
PIN_CONTROL_EXTRACTOR_2 = 22  
CANAL_PWM_EXTRACTOR_1 = 0  
CANAL_PWM_EXTRACTOR_2 = 1  

// Umbrales de gas  
FLOTANTE UMBRAL_BAJO = 100.0  
FLOTANTE UMBRAL_ALTO = 500.0  
ENTERO POTENCIA_EXTRACTOR = 0  
BOOLEANO ANULACION_MANUAL = FALSO  

Configuración Inicial  
FUNCION setup():  
    INICIALIZAR Serial  
    CONECTAR_WIFI(WIFI_SSID, WIFI_PASSWORD)  
    CONFIGURAR_MQTT(cliente_mqtt, MQTT_BROKER_IP, MQTT_BROKER_PORT)  
    SUSCRIBIR_MQTT(cliente_mqtt, MQTT_TOPIC_COMANDOS_EXTRACTORES)  
    CONFIGURAR_LoRa(868MHz, SF7, "receptor")  
    CONFIGURAR_EXTRACTORES()  
    APAGAR_EXTRACTORES()  

Bucle Principal  
FUNCION loop():  
    MANTENER_CONEXION_MQTT(cliente_mqtt)  
    MANTENER_CONEXION_WIFI()  
    PROCESAR_LORA()  

Procesamiento LoRa  
FUNCION PROCESAR_LORA():  
    mensaje_lora = RECIBIR_LORA()  
    objeto_datos_sensor = PARSEAR_JSON(mensaje_lora)  
    valor_gas = objeto_datos_sensor.valor  

    SI NO ANULACION_MANUAL:  
        CONTROL_AUTOMATICO_EXTRACTORES(valor_gas)  

    PUBLICAR_MQTT(cliente_mqtt, MQTT_TOPIC_SENSORES, mensaje_lora)  
    PUBLICAR_MQTT(cliente_mqtt, MQTT_TOPIC_ESTADO_EXTRACTORES, GENERAR_ESTADO_EXTRACTORES())  

Control de Extractores   
FUNCION CONTROL_AUTOMATICO_EXTRACTORES(valor_gas):  
    SI valor_gas >= UMBRAL_ALTO:  
        CONFIGURAR_EXTRACTORES(100)  
    SINO SI valor_gas >= UMBRAL_BAJO:  
        CONFIGURAR_EXTRACTORES(50)  
    SINO SI valor_gas < (UMBRAL_BAJO / 2):  
        APAGAR_EXTRACTORES()  

FUNCION CONFIGURAR_EXTRACTORES(potencia):  
    AJUSTAR_PWM(CANAL_PWM_EXTRACTOR_1, MAPEAR_POTENCIA(potencia))  
    AJUSTAR_PWM(CANAL_PWM_EXTRACTOR_2, MAPEAR_POTENCIA(potencia))  
    POTENCIA_EXTRACTOR = potencia  

FUNCION APAGAR_EXTRACTORES():  
    AJUSTAR_PWM(CANAL_PWM_EXTRACTOR_1, 0)  
    AJUSTAR_PWM(CANAL_PWM_EXTRACTOR_2, 0)  
    POTENCIA_EXTRACTOR = 0  

Manejo de Comandos MQTT  
FUNCION CALLBACK_MQTT_RECIBIDO(TEMA, MENSAJE):  
    objeto_comando = PARSEAR_JSON(MENSAJE)  
    ACCION = objeto_comando.accion  
    POTENCIA = objeto_comando.potencia  
    ANULACION_MANUAL = objeto_comando.anulacion_manual  

    SI ACCION ES IGUAL A "activar_alta":  
        CONFIGURAR_EXTRACTORES(100)  
    SINO SI ACCION ES IGUAL A "activar_baja":  
        CONFIGURAR_EXTRACTORES(50)  
    SINO SI ACCION ES IGUAL A "desactivar":  
        APAGAR_EXTRACTORES()  
    SINO SI ACCION ES IGUAL A "establecer_potencia":  
        CONFIGURAR_EXTRACTORES(POTENCIA)  

    PUBLICAR_MQTT(cliente_mqtt, MQTT_TOPIC_ESTADO_EXTRACTORES, GENERAR_ESTADO_EXTRACTORES())  

FIN  







