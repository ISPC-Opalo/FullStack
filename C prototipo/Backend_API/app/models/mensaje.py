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
    timestamp: datetime = Field(..., description="Fecha y hora del mensaje (YYYY-MM-DD HH:MM:SS)")
    sensor: SensorPayload
    control: ControlPayload
    estadoVentilador: str = Field(..., description="String detallado de estado del ventilador")

    class Config:
        extra = "ignore"

    @validator("timestamp", pre=True)
    def parse_timestamp(cls, v):
        """
        Espera una cadena como '2023-10-01 12:34:56' y la convierte a datetime.
        """
        if isinstance(v, datetime):
            return v
        try:
            return parser.parse(v)
        except ParserError as e:
            raise ValueError(f"timestamp inválido: {v}") from e

# ========================================
# EJEMPLO DE USO:
# data = json.loads(raw_payload)
# msg = GatewayMessage(**data)
# print(msg.sensor.ppm, msg.control.velocidad)
# ========================================