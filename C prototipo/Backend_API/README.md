## Documentacion de la API

-------------------------------------

### Funcion e intecnion
Esta aplicacion funciona como un middleware. Recibira los mensajes enviados en el topic "gas/datos" mediante el despleigue de un cliente MQTT, separara y ordenara la informacion recibida hacia el formato correcto y por ultimo registrara esta en la base de datos desplegada remotamente.

### Estrcutura

- 📦API
-  ┣ 📂app
-  ┃ ┣ 📂api
-  ┃ ┃ ┣ 📜routes.py
-  ┃ ┃ ┗ 📜__init__.py
-  ┃ ┣ 📂models
-  ┃ ┃ ┗ 📜mensaje.py
-  ┃ ┣ 📂services
-  ┃ ┃ ┗ 📜mysql_serv.py
-  ┃ ┣ 📂utils
-  ┃ ┃ ┗ 📜logger.py
-  ┃ ┣ 📜config.py
-  ┃ ┣ 📜main.py
-  ┃ ┣ 📜mqtt_listener.py
-  ┃ ┗ 📜__init__.py
-  ┣ 📜.env
-  ┣ 📜docker-compose.yml
-  ┣ 📜Readme.md
-  ┗ 📜requirements.txt

### Despliegue
La aplicacion se diseño para poder ser desplegada via docker dentro de cualquier entorno. Solo teniendo que modificar el archivo ".env"
Este documento muestra de forma clara los enpoints, usuarios, contraseñas y variables mediante los cuales se establece las conexiones de la misma

A considerar que esta diseñada para recibir un formato concreto y especifico, parsearlo y devolver otro formato fijo.
De queres reutilizar en otro proyecto se debera modificar los documentos de:
- [mensaje.py](C%prototipo/API/app/models/mensaje.py)
- [mysql_serv.py](C%prototipo/API/app/services/mysql_serv.py)

Estos se encargan de identificar el formato del mensaje recibido y pasearlo; y de los queries para ingresar los datos en la base de datos correspondiente

-------------------------------------

### Para a quien le interese el codigo como tal:

El **mqtt listener**. El cliente que funciona en segundo plano conectando con el/los topic configrados en el .env
Se encarga de:
- Conectar al broker MQTT
- Suscribirse a los topics indicados en settings.mqtt_topics
- Procesar cada mensaje y derivarlo al servicio adecuado. En esta caso a mysql_serv

[mqtt_listener.py](C%prototipo/Backend_API/app/mqtt_listener.py)

```py
class MQTTListener:
    #------------------------------------------
    # CREACION DEL CLIENTE MQTT
    #------------------------------------------
    def __init__(self):
        # Creamos el cliente MQTT
        self.client = mqtt.Client()
        # Si definimos que el broker requiere usuario/clave, descomentar:
        if settings.mqtt_user and settings.mqtt_password:
            self.client.username_pw_set(settings.mqtt_user, settings.mqtt_password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    #------------------------------------------
    # ARRAQUE DE CONEXION CON EL BROKER
    #------------------------------------------
    def start(self):
        logger.info(f"Conectando a broker MQTT en {settings.mqtt_broker_url}...")
        # Asumimos URL con puerto, ej: "mqtt://host:1883" -> extraemos host/puerto
        url = settings.mqtt_broker_url.replace("mqtt://", "")
        host, port = url.split(":")
        self.client.connect(host, int(port))
        # Levantamos el loop en background para no bloquear la app HTTP
        threading.Thread(target=self.client.loop_forever, daemon=True).start()
        logger.info("MQTT listener arrancado en background.")

    #------------------------------------------
    # ACCIONES AL CONECTAR (SUBSCRIPCION A TOPICS)
    #------------------------------------------
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Conexión MQTT exitosa.")
            # Nos suscribimos a cada topic, en caso de haber mas de uno
            for topic in settings.mqtt_topics:
                client.subscribe(topic)
                logger.info(f"Suscrito al topic '{topic}'.")
        else:
            logger.error(f"Fallo al conectar MQTT, código de error: {rc}")

    #------------------------------------------
    # ACCIONES AL RECIBIR MENSAJE
    #------------------------------------------
    def _on_message(self, client, userdata, msg):
        # Decodifica y parsea el JSON
        try:
            payload = msg.payload.decode("utf-8")
            data = json.loads(payload)
            logger.debug(f"Mensaje recibido en '{msg.topic}': {data}")
        except Exception as e:
            logger.error(f"Error parseando JSON en topic '{msg.topic}': {e}")
            return

        if any(msg.topic.startswith(t) for t in settings.mqtt_topics):
            try:
                # Validación del modelo de datos
                mensaje = GatewayMessage.parse_obj(data)
                # Guardado en ambos servicios
                mysql_serv.save_device_info(mensaje)
                logger.info("Guardado en MySQL e InfluxDB.")
            except Exception as ex:
                logger.error(f"Error guardando en servicios de BD: {ex}")
        else:
            logger.warning(f"Topic '{msg.topic}' no mapeado a ningún servicio.")


#------------------------------------------
# INTREGRACION EN MAIN.PY
#------------------------------------------
listener = MQTTListener()
```

**Modelo del mensaje**, gestionado por el documento [mensaje.py](C%prototipo/Backend_API/app/models/mensaje.py)
Este documento es el encargado de parsear el mensaje recibo. Esto implica, reconocerlo, identificar susparte, y separar/ordenarlo.
Luego sera pasado al o lo serviios, engardos de tomar esa data y registrarla donde corresponda.

```py
#========================================
# FORMATO DE LOS MENSAJES
#========================================

class SensorPayload(BaseModel):
    ppm: float = Field(..., description="Concentración en ppm")
    ratio: float = Field(..., description="Relación Rs/Ro")
    raw: int = Field(..., description="Valor bruto ADC")
    estado: str = Field(..., description="NORMAL o ALERTA")
    umbral: float = Field(..., description="Umbral configurado")

class ControlPayload(BaseModel):
    automatico: bool = Field(..., description="Modo automático activado")
    encendido: bool = Field(..., description="Extractor encendido")
    transicion: bool = Field(..., description="En transición de velocidad")
    velocidad: int = Field(..., description="Porcentaje de velocidad actual (0-100)")

class GatewayMessage(BaseModel):
    gatewayId: str = Field(..., description="Identificador del gateway")
    timestamp: int = Field(..., description="Milisegundos desde arranque")
    sensor: SensorPayload
    control: ControlPayload
    estadoVentilador: str = Field(..., description="String detallado de estado del ventilador")

    class Config:
        extra = "ignore"
```