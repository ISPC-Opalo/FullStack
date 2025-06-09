from pydantic import BaseModel, validator
from typing import Literal
from datetime import datetime


class SensorPayload(BaseModel):
    ppm: float
    ratio: float
    raw: int
    estado: Literal["NORMAL", "ALERTA"]
    umbral: float


class ControlPayload(BaseModel):
    automatico: bool
    encendido: bool
    transicion: bool
    velocidad: int


class ActuadorPayload(BaseModel):
    pin: int
    velocidad: int
    objetivo: int
    pwm_max: int
    encendido: bool
    transicion: bool


class GatewayMessage(BaseModel):
    gatewayId: str
    timestamp: datetime
    sensor: SensorPayload
    control: ControlPayload
    actuador: ActuadorPayload

    @validator("timestamp", pre=True)
    def parse_timestamp(cls, v):
        # Parseamos cadenas en formato dd/mm/YYYY HH:MM:SS
        if isinstance(v, str):
            return datetime.strptime(v, "%d/%m/%Y %H:%M:%S")
        return v


# ========================================
# EJEMPLO DE USO:
# data = json.loads(raw_payload)
# msg = GatewayMessage(**data)
# print(msg.sensor.ppm, msg.control.velocidad)
# ========================================