from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import (
    Table, MetaData, Column,
    Integer, String, DateTime, Float, ForeignKey, func
)
from app.utils.logger import get_logger
from app.models.mensaje import GatewayMessage
from app.config import settings

logger = get_logger("mysql_service")

#========================================
# Configuración SQLAlchemy
#========================================
_engine = sa.create_engine(settings.mysql_url)
_metadata = MetaData()

# 1) Tabla de dispositivos únicos
_dispositivo = Table(
    "dispositivo",
    _metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("device_id", String(64), nullable=False, unique=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    ),
)

# 2) Tabla de lecturas por dispositivo
_lecturas = Table(
    "lecturas",
    _metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "device_id",
        String(64),
        ForeignKey("dispositivo.device_id"),
        nullable=False
    ),
    Column("lectura", Float, nullable=False),
    Column("timestamp", DateTime(timezone=True), nullable=False),
)

# Crea las tablas si no existen
_metadata.create_all(_engine)


#========================================
# Función que registra info en MySQL
#========================================
def save_reading(msg: GatewayMessage) -> None:
    """
    1) Inserta el sensor en 'dispositivo' si no existe (INSERT IGNORE)
    2) Registra la lectura en 'lecturas' con el timestamp inyectado o parseado
    """
    sensor_id = msg.sensor.sensor_id
    lectura   = msg.sensor.lectura
    ts        = msg.timestamp  # viene ya con zoneinfo local

    logger.debug(f"Guardando lectura {lectura} de {sensor_id} @ {ts.isoformat()}")

    with _engine.begin() as conn:
        # a) Upsert mínimo para dispositivo
        ins_dev = sa.insert(_dispositivo).values(
            device_id=sensor_id
        ).prefix_with("IGNORE")  # MySQL: IGNORE duplicates
        conn.execute(ins_dev)

        # b) Inserta la lectura
        ins_lect = sa.insert(_lecturas).values(
            device_id=sensor_id,
            lectura=lectura,
            timestamp=ts
        )
        conn.execute(ins_lect)

    logger.info(f"Lectura almacenada para dispositivo {sensor_id}")