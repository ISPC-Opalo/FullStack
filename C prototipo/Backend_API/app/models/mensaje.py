from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from dateutil import parser
from dateutil.parser import ParserError

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

# ========================================
# EJEMPLO DE USO:
# data = json.loads(raw_payload)
# msg = GatewayMessage(**data)
# print(msg.sensor.ppm, msg.control.velocidad)
# ========================================