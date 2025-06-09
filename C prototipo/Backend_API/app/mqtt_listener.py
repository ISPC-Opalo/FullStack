import json
import threading
import paho.mqtt.client as mqtt
from datetime import datetime
from app.config import settings
from app.utils.logger import get_logger
from app.services import mariadb_serv
from app.models.mensaje import GatewayMessage

logger = get_logger("mqtt_listener")

#========================================
# Configuración de la aplicación (CLASE)
#========================================

class MQTTListener:
    """
    Se encarga de:
      - Conectar al broker MQTT
      - Suscribirse a los topics indicados en settings.mqtt_topics
      - Procesar cada mensaje y derivarlo al servicio adecuado. En esta caso a la base en MariaDB
    """
    #------------------------------------------
    # CREACION DEL CLIENTE MQTT
    #------------------------------------------
    def __init__(self):
        self.client = mqtt.Client()
        if settings.mqtt_user and settings.mqtt_password:
            self.client.username_pw_set(settings.mqtt_user, settings.mqtt_password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    #------------------------------------------
    # ARRAQUE DE CONEXION CON EL BROKER
    #------------------------------------------
    def start(self):
        logger.info(f"Conectando a broker MQTT en {settings.mqtt_broker_url}.")
        url = settings.mqtt_broker_url.replace("mqtt://", "")
        host, port = url.split(":")
        self.client.connect(host, int(port))
        threading.Thread(target=self.client.loop_forever, daemon=True).start()
        logger.info("MQTT listener arrancado en background.")

    #------------------------------------------
    # ACCIONES AL CONECTAR (SUBSCRIPCION A TOPICS)
    #------------------------------------------
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Conexión MQTT exitosa.")
            for topic in settings.mqtt_topics:
                client.subscribe(topic)
                logger.info(f"Suscrito al topic '{topic}'.")
        else:
            logger.error(f"Fallo al conectar MQTT, código de error: {rc}")

    #------------------------------------------
    # ACCIONES AL RECIBIR MENSAJE
    #------------------------------------------
    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode("utf-8").strip()
            # Eliminamos posibles comas finales que invalidan el JSON
            if payload.endswith(",}"):
                payload = payload.replace(",}", "}")
            raw_data = json.loads(payload)
            logger.info(f"Mensaje recibido en '{msg.topic}': {raw_data}")

            mensaje = GatewayMessage.parse_obj(raw_data)
            mariadb_serv.guardarDatos(mensaje)
            logger.info("Guardado en MariaDB.")
        except Exception as e:
            logger.error(f"Error procesando mensaje de topic '{msg.topic}': {e}")



#------------------------------------------
# INTREGRACION EN MAIN.PY
#------------------------------------------
listener = MQTTListener()
