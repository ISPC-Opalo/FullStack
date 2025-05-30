# database.py

import pymysql
import os
import logging
from datetime import datetime, timedelta

# Configuración del Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Nivel de log: INFO, WARNING, ERROR, DEBUG
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configuración de la Base de Datos
# Se recomienda encarecidamente usar variables de entorno para las credenciales.
# Si no se encuentran las variables de entorno, se usarán valores por defecto (ej. para desarrollo local).
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"), # ¡CAMBIA ESTO EN PRODUCCIÓN POR UN USUARIO DEDICADO!
    "password": os.getenv("DB_PASSWORD", ""), # ¡CAMBIA ESTO EN PRODUCCIÓN!
    "database": os.getenv("DB_NAME", "iot_gases"),
    "autocommit": True, # Asegura que las operaciones de inserción se guarden automáticamente.
    "charset": "utf8mb4", # Soporte para caracteres UTF-8.
    "cursorclass": pymysql.cursors.DictCursor # Importante: para que los resultados de SELECT sean diccionarios
}

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL/MariaDB.
    Maneja excepciones en caso de fallo en la conexión.

    Retorna:
        pymysql.connections.Connection: Un objeto de conexión a la base de datos, o None si falla.
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        # logger.info("Conexión a la base de datos establecida.") # Descomentar para debug intenso
        return conn
    except pymysql.Error as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None

# Funciones de Inserción
def insert_sensor_data(data: dict) -> bool:
    """
    Inserta un registro de datos de sensor en la tabla `registros_sensores`.

    Args:
        data (dict): Un diccionario con los datos del sensor.
                     Debe contener 'id_dispositivo', 'valor' y opcionalmente 'tipo_dato', 'timestamp'.
                     Ejemplo: {'id_dispositivo': 'SENSOR_GAS_01', 'tipo_dato': 'concentracion_gas', 'valor': 123.45, 'timestamp': '2023-10-27T10:00:00'}

    Retorna:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO registros_sensores (id_dispositivo, tipo_dato, valor_ppm, timestamp)
            VALUES (%s, %s, %s, %s)
            """
            
            # Intenta parsear el timestamp si viene como string en formato ISO, si no usa la hora actual
            timestamp_dt = datetime.now()
            if 'timestamp' in data and isinstance(data['timestamp'], str):
                try:
                    timestamp_dt = datetime.fromisoformat(data['timestamp'])
                except ValueError:
                    logger.warning(f"Formato de timestamp inválido '{data['timestamp']}'. Usando la hora actual de la API.")
            elif 'timestamp' in data and isinstance(data['timestamp'], datetime):
                timestamp_dt = data['timestamp']
            else:
                logger.warning(f"Timestamp no proporcionado o tipo incorrecto. Usando la hora actual de la API.")

            cursor.execute(sql, (
                data.get("id_dispositivo"),
                data.get("tipo_dato", "concentracion_gas"), # Valor por defecto si no se proporciona
                data.get("valor"),
                timestamp_dt
            ))
        logger.info(f"Datos de sensor insertados: Dispositivo={data.get('id_dispositivo')}, Valor={data.get('valor')} PPM")
        return True
    except pymysql.Error as e:
        logger.error(f"Error al insertar datos de sensor en DB: {e}")
        return False
    finally:
        if conn:
            conn.close()

def insert_extractor_history(
    timestamp: datetime,
    tipo_control: str,
    potencia_ajustada: int,
    razon_ajuste: str = None,
    valor_gas_ppm: float = None
) -> bool:
    """
    Inserta un registro en la tabla `historial_extractores` para documentar un evento de control.

    Args:
        timestamp (datetime): Fecha y hora del evento.
        tipo_control (str): Tipo de control ('automatico' o 'manual').
        potencia_ajustada (int): Nivel de potencia (%) al que se ajustaron los extractores.
        razon_ajuste (str, optional): Razón del ajuste. Por defecto es None.
        valor_gas_ppm (float, optional): Concentración de gas en PPM en el momento del ajuste. Por defecto es None.

    Retorna:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO historial_extractores (timestamp, tipo_control, potencia_ajustada, razon_ajuste, valor_gas_ppm)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                timestamp,
                tipo_control,
                potencia_ajustada,
                razon_ajuste,
                valor_gas_ppm
            ))
        logger.info(f"Historial de extractor insertado: Tipo={tipo_control}, Potencia={potencia_ajustada}%")
        return True
    except pymysql.Error as e:
        logger.error(f"Error al insertar historial de extractor en DB: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Funciones de Consulta

def get_latest_sensor_data(device_id: str = None) -> dict | None:
    """
    Obtiene la última lectura de gas de un dispositivo específico o la última de cualquier dispositivo.

    Args:
        device_id (str, optional): El ID del dispositivo a consultar. Si es None, busca la última de cualquier dispositivo.

    Retorna:
        dict | None: Un diccionario con los datos de la última lectura, o None si no se encuentran datos.
    """
    conn = get_db_connection()
    if not conn: return None
    try:
        with conn.cursor() as cursor:
            if device_id:
                sql = """
                SELECT id_registro, id_dispositivo, tipo_dato, valor_ppm, timestamp
                FROM registros_sensores
                WHERE id_dispositivo = %s
                ORDER BY timestamp DESC
                LIMIT 1;
                """
                cursor.execute(sql, (device_id,))
            else:
                sql = """
                SELECT id_registro, id_dispositivo, tipo_dato, valor_ppm, timestamp
                FROM registros_sensores
                ORDER BY timestamp DESC
                LIMIT 1;
                """
                cursor.execute(sql)
            
            result = cursor.fetchone() # fetchone() retorna una sola fila
            return result
    except pymysql.Error as e:
        logger.error(f"Error al obtener la última lectura del sensor: {e}")
        return None
    finally:
        if conn: conn.close()

def get_sensor_data_by_time_range(
    start_time: datetime,
    end_time: datetime,
    device_id: str = None,
    limit: int = 100
) -> list[dict] | None:
    """
    Obtiene lecturas de gas dentro de un rango de tiempo específico.

    Args:
        start_time (datetime): La fecha y hora de inicio del rango.
        end_time (datetime): La fecha y hora de fin del rango.
        device_id (str, optional): El ID del dispositivo a consultar. Si es None, busca de todos los dispositivos.
        limit (int): El número máximo de registros a retornar. Por defecto 100.

    Retorna:
        list[dict] | None: Una lista de diccionarios con los datos de las lecturas, o None si falla.
    """
    conn = get_db_connection()
    if not conn: return None
    try:
        with conn.cursor() as cursor:
            params = [start_time, end_time]
            sql = """
            SELECT id_registro, id_dispositivo, tipo_dato, valor_ppm, timestamp
            FROM registros_sensores
            WHERE timestamp BETWEEN %s AND %s
            """
            if device_id:
                sql += " AND id_dispositivo = %s"
                params.append(device_id)
            
            sql += " ORDER BY timestamp ASC LIMIT %s;"
            params.append(limit)

            cursor.execute(sql, tuple(params))
            
            results = cursor.fetchall() # fetchall() retorna todas las filas
            return results
    except pymysql.Error as e:
        logger.error(f"Error al obtener datos de sensor por rango de tiempo: {e}")
        return None
    finally:
        if conn: conn.close()

def get_all_extractor_history(limit: int = 100) -> list[dict] | None:
    """
    Obtiene el historial completo de control de extractores.

    Args:
        limit (int): El número máximo de registros a retornar. Por defecto 100.

    Retorna:
        list[dict] | None: Una lista de diccionarios con los eventos del historial, o None si falla.
    """
    conn = get_db_connection()
    if not conn: return None
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT id_evento, timestamp, tipo_control, potencia_ajustada, razon_ajuste, valor_gas_ppm
            FROM historial_extractores
            ORDER BY timestamp DESC
            LIMIT %s;
            """
            cursor.execute(sql, (limit,))
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        logger.error(f"Error al obtener el historial de extractores: {e}")
        return None
    finally:
        if conn: conn.close()

def get_extractor_history_by_control_type(control_type: str, limit: int = 100) -> list[dict] | None:
    """
    Obtiene el historial de control de extractores filtrado por tipo de control (automático/manual).

    Args:
        control_type (str): El tipo de control ('automatico' o 'manual').
        limit (int): El número máximo de registros a retornar. Por defecto 100.

    Retorna:
        list[dict] | None: Una lista de diccionarios con los eventos, o None si falla.
    """
    conn = get_db_connection()
    if not conn: return None
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT id_evento, timestamp, tipo_control, potencia_ajustada, razon_ajuste, valor_gas_ppm
            FROM historial_extractores
            WHERE tipo_control = %s
            ORDER BY timestamp DESC
            LIMIT %s;
            """
            cursor.execute(sql, (control_type, limit))
            results = cursor.fetchall()
            return results
    except pymysql.Error as e:
        logger.error(f"Error al obtener historial de extractores por tipo de control: {e}")
        return None
    finally:
        if conn: conn.close()

# Bloque de prueba (solo para este archivo, se ejecuta si corres `python database.py`)
if __name__ == "__main__":
    # Para probar este módulo directamente, asegúrate de que tus variables de entorno estén configuradas
    # o de lo contrario ajusta los valores por defecto en DB_CONFIG.
    from dotenv import load_dotenv
    load_dotenv() # Carga las variables de entorno del archivo .env al ejecutar este script

    logger.info ( "Iniciando pruebas de funciones de la base de datos (database.py)")

    # PRUEBAS DE INSERCIÓN (para asegurar que tenemos datos para consultar)
    logger.info("Realizando inserciones de prueba para asegurar datos para las consultas...")
    insert_sensor_data({
        "id_dispositivo": "SENSOR_GAS_01",
        "valor": 120.5,
        "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat()
    })
    insert_sensor_data({
        "id_dispositivo": "SENSOR_GAS_02",
        "valor": 80.0,
        "timestamp": (datetime.now() - timedelta(minutes=3)).isoformat()
    })
    insert_sensor_data({
        "id_dispositivo": "SENSOR_GAS_01",
        "valor": 150.7,
        "timestamp": datetime.now().isoformat()
    })
    insert_extractor_history(
        timestamp=datetime.now() - timedelta(minutes=2),
        tipo_control="automatico",
        potencia_ajustada=50,
        razon_ajuste="Umbral bajo",
        valor_gas_ppm=100.0
    )
    insert_extractor_history(
        timestamp=datetime.now() - timedelta(minutes=1),
        tipo_control="manual",
        potencia_ajustada=100,
        razon_ajuste="Prueba manual"
    )
    logger.info("Inserciones de prueba completadas.\n")

    # EJEMPLOS DE CONSULTA

    # 1. Obtener la última lectura de cualquier sensor
    logger.info("1. Obteniendo la última lectura de cualquier sensor:")
    latest_data = get_latest_sensor_data()
    if latest_data:
        logger.info(f"Última lectura: {latest_data}")
    else:
        logger.warning("No se encontraron datos de sensores.")

    # 2. Obtener la última lectura de un sensor específico
    logger.info("\n2. Obteniendo la última lectura del SENSOR_GAS_01:")
    latest_data_s1 = get_latest_sensor_data(device_id="SENSOR_GAS_01")
    if latest_data_s1:
        logger.info(f"Última lectura SENSOR_GAS_01: {latest_data_s1}")
    else:
        logger.warning("No se encontraron datos para SENSOR_GAS_01.")

    # 3. Obtener datos de sensores en un rango de tiempo (últimos 10 minutos)
    logger.info("\n3. Obteniendo lecturas de sensores en los últimos 10 minutos (todos los dispositivos):")
    end_time_range = datetime.now()
    start_time_range = end_time_range - timedelta(minutes=10)
    data_in_range = get_sensor_data_by_time_range(start_time=start_time_range, end_time=end_time_range)
    if data_in_range:
        for row in data_in_range:
            logger.info(f"  - {row}")
    else:
        logger.warning("No se encontraron datos de sensores en el rango especificado.")

    # 4. Obtener datos de un sensor específico en un rango de tiempo
    logger.info("\n4. Obteniendo lecturas de SENSOR_GAS_01 en los últimos 10 minutos:")
    data_s1_in_range = get_sensor_data_by_time_range(start_time=start_time_range, end_time=end_time_range, device_id="SENSOR_GAS_01")
    if data_s1_in_range:
        for row in data_s1_in_range:
            logger.info(f"  - {row}")
    else:
        logger.warning("No se encontraron datos para SENSOR_GAS_01 en el rango especificado.")

    # 5. Obtener todo el historial de extractores
    logger.info("\n5. Obteniendo todo el historial de extractores:")
    extractor_history = get_all_extractor_history()
    if extractor_history:
        for row in extractor_history:
            logger.info(f"  - {row}")
    else:
        logger.warning("No se encontró historial de extractores.")

    # 6. Obtener historial de extractores por tipo de control
    logger.info("\n6. Obteniendo historial de extractores automáticos:")
    auto_history = get_extractor_history_by_control_type(control_type="automatico")
    if auto_history:
        for row in auto_history:
            logger.info(f"  - {row}")
    else:
        logger.warning("No se encontró historial de extractores automáticos.")
    logger.info ("Fin de las pruebas de las funciones de la base de datos")