from typing import List
from fastapi import HTTPException
from fastapi import Depends
from fastapi import status
from fastapi import APIRouter

from app.config import settings
from app.models.mensaje import GatewayMessage
from app.services import mysql_serv, influx_serv

router = APIRouter()

#========================================
# LISTA DE ROUTAS DE LA API
#========================================

#------------------------------------------
# RUTAS DE LOS TOPICS DEFINIDOS EN SETTINGS
#------------------------------------------
@router.get("/topics", response_model=List[str], status_code=status.HTTP_200_OK)
async def list_topics():
    return settings.mqtt_topics


#------------------------------------------
# DEVUELVE LOS ULTIMOS MENSAJES DE MYSQL E INFLUXDB
#------------------------------------------
@router.get("/messages", response_model=List[GatewayMessage], status_code=status.HTTP_200_OK)
async def read_messages():
    """
    Obtiene los últimos mensajes de MySQL e InfluxDB.
    Actualmente es un placeholder; implementa según tu esquema de BD.
    """
    result: List[GatewayMessage] = []
    try:
        result += mysql_serv.get_recent_messages()
    except Exception:
        raise HTTPException(status_code=500, detail="Error al leer de MySQL")
    try:
        result += influx_serv.get_recent_messages()
    except Exception:
        raise HTTPException(status_code=500, detail="Error al leer de InfluxDB")
    return result
