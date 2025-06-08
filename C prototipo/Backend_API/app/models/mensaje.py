from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from dateutil import parser
from dateutil.parser import ParserError
from typing import Union


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
    gatewayId: str
    timestamp: str  # ← ahora esperamos un string tipo "08/06/2025 16:30:44"
    sensor: SensorPayload
    control: ControlPayload
    estadoVentilador: str

    @validator("timestamp", pre=True)
    def validar_formato_timestamp(cls, v):
        try:
            # Validamos formato, pero no lo convertimos
            datetime.strptime(v, "%d/%m/%Y %H:%M:%S")
            return v
        except ValueError:
            raise ValueError("El timestamp debe estar en formato DD/MM/YYYY HH:MM:SS")

# ========================================
# EJEMPLO DE USO:
# data = json.loads(raw_payload)
# msg = GatewayMessage(**data)
# print(msg.sensor.ppm, msg.control.velocidad)
# ========================================