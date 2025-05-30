# main.py

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import threading
import logging
import os
from dotenv import load_dotenv # Para cargar variables de entorno
from datetime import datetime # Para tipos en los modelos Pydantic

# Cargar variables de entorno del archivo .env
load_dotenv()

# Importar las funciones de nuestros modulos
from database import ( # type: ignore
    get_db_connection,
    insert_sensor_data, # Aunque no se usa directamente en endpoints, se usa en mqtt_client.py
    insert_extractor_history, # Ídem
    get_latest_sensor_data,
    get_sensor_data_by_time_range,
    get_all_extractor_history,
    get_extractor_history_by_control_type
)
from mqtt_client import get_mqtt_client, start_mqtt_loop, MQTT_TOPIC_COMANDOS_EXTRACTORES
import json

# --- Configuracion del Logger para FastAPI ---
# Configura el logger principal para la aplicacion FastAPI.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Instancia de FastAPI ---
app = FastAPI(
    title="API de Monitoreo de Gases",
    description="Sistema IoT para el monitoreo de gases y control de extractores con ESP32, LoRa, MQTT y FastAPI.",
    version="1.0.0",
    docs_url="/docs",       # URL para la documentacion interactiva (Swagger UI)
    redoc_url="/redoc"      # URL para la documentacion alternativa (ReDoc)
)

# --- Modelos Pydantic para los datos (validacion de entrada y documentacion) ---
# Usados para la documentacion interactiva de la API y la validacion automática de datos.
class SensorDataResponse(BaseModel):
    id_registro: int
    id_dispositivo: str
    tipo_dato: str
    valor_ppm: float
    timestamp: datetime

class ExtractorHistoryResponse(BaseModel):
    id_evento: int
    timestamp: datetime
    tipo_control: str
    potencia_ajustada: int
    razon_ajuste: str | None # Union[str, None]
    valor_gas_ppm: float | None # Union[float, None]

class ExtractorCommandPayload(BaseModel):
    accion: str # Ej. "activar_alta", "activar_baja", "desactivar", "establecer_potencia"
    potencia: int | None = None # Opcional, para "establecer_potencia"
    anulacion_manual: bool = False # Para que el Nodo Central sepa si ignorar el control automático

# --- Rutas de FastAPI (Endpoints de la API REST) ---

@app.get("/", summary="Endpoint raíz", response_description="Mensaje de bienvenida de la API.")
async def root():
    """
    Endpoint de bienvenida para la API de Monitoreo de Gases.
    """
    return {"message": "Bienvenido a la API de Monitoreo de Gases con FastAPI y MQTT"}

@app.get("/status/db", summary="Verificar estado de la base de datos", response_description="Estado de la conexion a la base de datos.")
async def db_status():
    """
    Verifica si la aplicacion puede conectarse correctamente a la base de datos MySQL/MariaDB.
    """
    conn = get_db_connection()
    if conn:
        conn.close()
        logger.info("Conexion a la base de datos exitosa desde /status/db.")
        return {"status": "connected", "message": "Conexion a la base de datos exitosa."}
    else:
        logger.error("Fallo al conectar a la base de datos desde /status/db.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Fallo al conectar a la base de datos. Verifica las credenciales y el servidor.")

@app.get("/data/latest_gas", response_model=SensorDataResponse | dict, summary="Última lectura de gas",
            response_description="Retorna la última lectura de concentracion de gas de cualquier sensor o de uno específico.")
async def get_latest_gas_reading(device_id: str | None = None):
    """
    **Obtiene la última lectura de gas registrada en la base de datos.**

    - **`device_id` (opcional):** Filtra por el ID de un dispositivo sensor específico (ej. "SENSOR_GAS_01").
    """
    try:
        latest_data = get_latest_sensor_data(device_id)
        if latest_data:
            return SensorDataResponse(**latest_data) # Valida y retorna el modelo Pydantic
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron datos de gas.")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error al obtener la última lectura de gas: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")

@app.get("/data/gas_by_range", response_model=list[SensorDataResponse], summary="Lecturas de gas por rango de tiempo",
            response_description="Retorna las lecturas de concentracion de gas dentro de un rango de tiempo definido.")
async def get_gas_readings_by_range(
    start_time: datetime,
    end_time: datetime = datetime.now(), # Por defecto, la hora actual
    device_id: str | None = None,
    limit: int = 100
):
    """
    **Obtiene lecturas de gas de la base de datos dentro de un rango de tiempo.**

    - **`start_time` (Requerido):** Fecha y hora de inicio del rango (formato ISO 8601, ej. '2023-10-26T00:00:00').
    - **`end_time` (Opcional):** Fecha y hora de fin del rango (por defecto, la hora actual).
    - **`device_id` (Opcional):** Filtra por el ID de un dispositivo sensor específico.
    - **`limit` (Opcional):** Número máximo de registros a retornar (por defecto 100).
    """
    if start_time >= end_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="start_time debe ser anterior a end_time.")
    try:
        data = get_sensor_data_by_time_range(start_time, end_time, device_id, limit)
        if data:
            return [SensorDataResponse(**item) for item in data] # Mapea los resultados a la lista de modelos
        return [] # Retorna una lista vacía si no hay datos en el rango
    except Exception as e:
        logger.error(f"Error al obtener lecturas de gas por rango: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")

@app.get("/history/extractors", response_model=list[ExtractorHistoryResponse], summary="Historial de extractores",
            response_description="Retorna el historial de control de los extractores.")
async def get_extractors_history(control_type: str | None = None, limit: int = 100):
    """
    **Obtiene el historial de control de los extractores.**

    - **`control_type` (opcional):** Filtra por tipo de control ('automatico' o 'manual').
    - **`limit` (opcional):** Número máximo de registros a retornar (por defecto 100).
    """
    try:
        if control_type:
            if control_type not in ["automatico", "manual"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El tipo de control debe ser 'automatico' o 'manual'.")
            history = get_extractor_history_by_control_type(control_type, limit)
        else:
            history = get_all_extractor_history(limit)
        
        if history:
            return [ExtractorHistoryResponse(**item) for item in history] # Mapea los resultados a la lista de modelos
        return []
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error al obtener el historial de extractores: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")

@app.post("/commands/send_extractor", status_code=status.HTTP_202_ACCEPTED, summary="Enviar comando a extractores",
            response_description="Estado de la publicacion del comando MQTT.")
async def send_extractor_command(command: ExtractorCommandPayload):
    """
    **Permite enviar comandos de control a los extractores a través de MQTT.**

    Este endpoint simula una aplicacion movil o una interfaz de usuario controlando los extractores.
    El Nodo Central LoRa de tu sistema estará suscrito al topico MQTT donde se publican estos comandos.

    - **`accion` (Requerido):** Tipo de accion (ej. "activar_alta", "activar_baja", "desactivar", "establecer_potencia").
    - **`potencia` (Opcional):** Nivel de potencia (0-100) si la accion es "establecer_potencia".
    - **`anulacion_manual` (Opcional):** Booleano que indica si este comando anula el control automático del Nodo Central.
    """
    try:
        mqtt_client = get_mqtt_client()
        # Asegúrate de que el cliente MQTT esté conectado antes de intentar publicar
        if not mqtt_client.is_connected():
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="El cliente MQTT no está conectado. Inténtalo de nuevo más tarde.")

        # Convierte el modelo Pydantic a un diccionario, excluyendo campos no establecidos para un JSON más limpio
        payload = json.dumps(command.dict(exclude_unset=True))
        mqtt_client.publish(MQTT_TOPIC_COMANDOS_EXTRACTORES, payload)
        logger.info(f"Comando MQTT publicado a '{MQTT_TOPIC_COMANDOS_EXTRACTORES}': {payload}")
        return {"status": "success", "message": "Comando MQTT publicado exitosamente."}
    except HTTPException as e:
        raise e # Re-lanzar las excepciones HTTP para que FastAPI las maneje
    except Exception as e:
        logger.error(f"Error al publicar comando MQTT: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error interno del servidor al publicar comando MQTT: {e}")


# --- Eventos de inicio y apagado de FastAPI ---

@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicacion FastAPI.
    Inicia el bucle de MQTT en un hilo separado para no bloquear el servidor web.
    """
    logger.info("Iniciando la aplicacion FastAPI...")
    mqtt_thread = threading.Thread(target=start_mqtt_loop, daemon=True)
    mqtt_thread.start()
    logger.info("Hilo de cliente MQTT iniciado en segundo plano.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al apagar la aplicacion FastAPI.
    Desconecta el cliente MQTT de forma limpia.
    """
    logger.info("Apagando la aplicacion FastAPI...")
    mqtt_client = get_mqtt_client()
    if mqtt_client.is_connected():
        logger.info("Desconectando cliente MQTT...")
        mqtt_client.disconnect()
        logger.info("Cliente MQTT desconectado.")
    else:
        logger.info("Cliente MQTT no estaba conectado o ya se desconecto.")