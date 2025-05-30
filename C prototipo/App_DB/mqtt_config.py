# mqtt_config.py

import paho.mqtt.client as mqtt
import os
import json
import logging
from datetime import datetime
import time
import threading

# Importar las funciones de base de datos
from database import insert_sensor_data, insert_extractor_history

# --- Configuración del Logger ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# --- Configuración de MQTT desde variables de entorno ---
MQTT_BROKER_IP = os.getenv("MQTT_BROKER_IP", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC_SENSORES = "sensores/data"
MQTT_TOPIC_COMANDOS_EXTRACTORES = "acciones/comandos_extractores"
MQTT_TOPIC_ESTADO_EXTRACTORES = "acciones/estado_extractores"

mqtt_client_instance = None # Instancia global para el cliente MQTT

def on_connect(client, userdata, flags, rc):
    """Callback cuando el cliente se conecta al broker MQTT."""
    if rc == 0:
        logger.info("Conectado al broker MQTT exitosamente!")
        # Suscribirse a los tópicos relevantes para recibir datos y estados
        client.subscribe(MQTT_TOPIC_SENSORES)
        client.subscribe(MQTT_TOPIC_ESTADO_EXTRACTORES)
        # Suscribirse al tópico de comandos para "escuchar" lo que la app móvil envía al Nodo Central
        client.subscribe(MQTT_TOPIC_COMANDOS_EXTRACTORES) 
        logger.info(f"Suscrito a los tópicos: {MQTT_TOPIC_SENSORES}, {MQTT_TOPIC_ESTADO_EXTRACTORES}, {MQTT_TOPIC_COMANDOS_EXTRACTORES}")
    else:
        logger.error(f"Fallo la conexión al broker MQTT con código: {rc}")

def on_message(client, userdata, msg):
    """Callback cuando se recibe un mensaje MQTT."""
    try:
        payload = msg.payload.decode()
        logger.info(f"Mensaje recibido del tópico '{msg.topic}': {payload}")

        data = json.loads(payload)

        current_time_api_received = datetime.now() # Hora en que la API recibió el mensaje

        # Procesa mensajes del tópico de sensores y los inserta en la DB
        if msg.topic == MQTT_TOPIC_SENSORES:
            # Asegurarse de que 'valor' y 'id_dispositivo' existan
            if "valor" in data and "id_dispositivo" in data:
                # Pasar el diccionario 'data' directamente a insert_sensor_data.
                # La función de DB manejará el 'timestamp' si es string o si no está presente.
                insert_sensor_data(data)
            else:
                logger.warning(f"Mensaje de sensor incompleto en tópico '{msg.topic}': {data}")

        # Procesa mensajes del tópico de estado de extractores y los inserta en la DB
        elif msg.topic == MQTT_TOPIC_ESTADO_EXTRACTORES:
            # Asume que el Nodo Central publica el estado de los extractores con 'potencia_actual', 'tipo_control', 'razon'
            if "potencia_actual" in data and "tipo_control" in data:
                insert_extractor_history(
                    timestamp=current_time_api_received, # Usar la hora de recepción para el historial de eventos de la API
                    tipo_control=data.get("tipo_control"),
                    potencia_ajustada=data.get("potencia_actual"),
                    razon_ajuste=data.get("razon", None),
                    valor_gas_ppm=data.get("valor_gas_ppm_en_ese_momento", None)
                )
            else:
                logger.warning(f"Mensaje de estado de extractor incompleto en tópico '{msg.topic}': {data}")

        # Procesa mensajes del tópico de comandos (para loguear comandos manuales de la app)
        # Esto es útil para auditar qué comandos se enviaron desde la app móvil.
        elif msg.topic == MQTT_TOPIC_COMANDOS_EXTRACTORES:
            logger.info(f"Comando de extractor recibido vía MQTT (potencialmente desde app móvil): {data}")
            accion = data.get("accion")
            potencia = data.get("potencia", 0) # Si la acción es 'desactivar', potencia podría ser 0
            if accion:
                insert_extractor_history(
                    timestamp=current_time_api_received,
                    tipo_control="manual",
                    potencia_ajustada=potencia,
                    razon_ajuste=f"Comando manual recibido: {accion}",
                    valor_gas_ppm=None # No hay un valor de gas directo asociado a un comando puro
                )
            else:
                logger.warning(f"Comando de extractor incompleto en tópico '{msg.topic}': {data}")


    except json.JSONDecodeError:
        logger.error(f"Error al decodificar JSON del mensaje en tópico '{msg.topic}': {payload}")
    except Exception as e:
        logger.error(f"Error general en on_message para tópico '{msg.topic}': {e}", exc_info=True) # exc_info para stack trace

def get_mqtt_client():
    """Retorna la instancia del cliente MQTT global."""
    global mqtt_client_instance
    if mqtt_client_instance is None:
        mqtt_client_instance = mqtt.Client()
        mqtt_client_instance.on_connect = on_connect
        mqtt_client_instance.on_message = on_message
    return mqtt_client_instance

def start_mqtt_loop():
    """
    Inicia el bucle de MQTT en un hilo separado y maneja la reconexión automática.
    """
    client = get_mqtt_client()
    while True:
        try:
            logger.info(f"Intentando conectar a MQTT broker en {MQTT_BROKER_IP}:{MQTT_BROKER_PORT}...")
            client.connect(MQTT_BROKER_IP, MQTT_BROKER_PORT, 60)
            client.loop_forever() # Bloquea el hilo, por eso debe estar en un hilo separado
        except Exception as e:
            logger.error(f"No se pudo conectar al broker MQTT o conexión perdida: {e}. Reintentando en 5 segundos...", exc_info=True)
            time.sleep(5)
        # Si loop_forever() termina (ej. por desconexión), el bucle `while True` intentará reconectar.