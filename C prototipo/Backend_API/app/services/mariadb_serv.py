from typing import Optional
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, Boolean, Text, ForeignKey, select, DateTime
from sqlalchemy.exc import OperationalError
from app.utils.logger import get_logger
from app.models.mensaje import GatewayMessage
from app.config import settings


logger = get_logger("mariadb_service")

#========================================
# Configuración SQLAlchemy con pool settings
#========================================
_engine = sa.create_engine(
    settings.mariadb_url,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)
_metadata = MetaData()

#========================================
# Definición de tablas según nuevo esquema
#========================================
_dispositivo_table = Table(
    "dispositivo",
    _metadata,
    Column("dispositivo_id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(50), nullable=False),
    Column("descripcion", String(100)),
    Column("ubicacion", String(100)),
)

_sensor_table = Table(
    "sensor",
    _metadata,
    Column("sensor_id", Integer, primary_key=True, autoincrement=True),
    Column("dispositivo_id", Integer, ForeignKey("dispositivo.dispositivo_id"), nullable=False),
    Column("ppm", Float, nullable=False),
    Column("valor", Float, nullable=False),
    Column("crudo", Integer, nullable=False),
    Column("estado_sensor", String(20), nullable=False),
    Column("umbral", Float, nullable=False),
)

_medicion_table = Table(
    "medicion",
    _metadata,
    Column("medicion_id", Integer, primary_key=True, autoincrement=True),
    Column("dispositivo_id", Integer, ForeignKey("dispositivo.dispositivo_id"), nullable=False),
    Column("auto", Boolean, nullable=False),
    Column("encendido", Boolean, nullable=False),
    Column("vel_actual", Integer, nullable=False),
    Column("vel_objetivo", Integer, nullable=False),
    Column("transicion", Boolean, nullable=False),
    Column("timestamp", DateTime, nullable=False),
)

_actuador_table = Table(
    "actuador",
    _metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("medicion_id", Integer, ForeignKey("medicion.medicion_id"), nullable=False),
    Column("pin", Integer, nullable=False),
    Column("velocidad", Integer, nullable=False),
    Column("objetivo", Integer, nullable=False),
    Column("encendido", Boolean, nullable=False),
    Column("transicion", Boolean, nullable=False),
    Column("pwm_max", Integer, nullable=False),
    Column("nombre", String(50)),
)

# Crear tablas si no existen
_metadata.create_all(_engine)

#========================================
# Función que registra info en MariaDB con manejo de errores y logs
#========================================
def guardarDatos(msg: GatewayMessage) -> None:
    logger.debug(f"Guardando mensaje en MariaDB: {msg}")
    try:
        with _engine.begin() as conn:
            # 1) Dispositivo
            gateway = msg.gatewayId
            sel = select(_dispositivo_table.c.dispositivo_id).where(
                _dispositivo_table.c.nombre == gateway
            )
            dispositivo_id = conn.execute(sel).scalar()
            if dispositivo_id is None:
                res = conn.execute(
                    sa.insert(_dispositivo_table).values(nombre=gateway)
                )
                dispositivo_id = res.inserted_primary_key[0]
                logger.info(f"Dispositivo creado con ID {dispositivo_id}")
            else:
                logger.debug(f"Dispositivo existente ID {dispositivo_id}")

            # 2) Sensor
            sensor = msg.sensor
            conn.execute(
                sa.insert(_sensor_table).values(
                    dispositivo_id=dispositivo_id,
                    ppm=sensor.ppm,
                    valor=sensor.ratio,
                    crudo=sensor.raw,
                    estado_sensor=sensor.estado,
                    umbral=sensor.umbral,
                )
            )
            logger.debug("Datos de sensor insertados")

            # 3) Medición
            control = msg.control
            ts_datetime = msg.timestamp
            res_m = conn.execute(
                sa.insert(_medicion_table).values(
                    dispositivo_id=dispositivo_id,
                    auto=control.automatico,
                    encendido=control.encendido,
                    vel_actual=control.velocidad,
                    vel_objetivo=msg.actuador.objetivo,
                    transicion=control.transicion,
                    timestamp=ts_datetime,
                )
            )
            medicion_id = res_m.inserted_primary_key[0]
            logger.debug(f"Medición insertada con ID {medicion_id}")

            # 4) Actuador
            actuador = msg.actuador
            conn.execute(
                sa.insert(_actuador_table).values(
                    medicion_id=medicion_id,
                    pin=actuador.pin,
                    velocidad=actuador.velocidad,
                    objetivo=actuador.objetivo,
                    encendido=actuador.encendido,
                    transicion=actuador.transicion,
                    nombre="ventilador"
                )
            )
            logger.debug("Registro de actuador insertado")

        logger.info("Datos registrados correctamente en MariaDB.")
    except OperationalError as oe:
        logger.error(f"OperationalError al acceder a MariaDB: {oe}")
    except Exception as e:
        logger.error(f"Error inesperado al guardar datos en MariaDB: {e}")

