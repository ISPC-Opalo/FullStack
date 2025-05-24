from datetime import datetime
from pydantic import BaseModel, Field, root_validator
from dateutil import parser

class SensorSimple(BaseModel):
    sensor_id: str = Field(..., alias="sensor ID")
    lectura: float

class GatewayMessage(BaseModel):
    gateway_id: str = Field(..., alias="Gateway ID")
    sensor: SensorSimple
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now().astimezone(),
        description="Marca de tiempo local del servidor"
    )

    @root_validator(pre=True)
    def remap_and_validate(cls, values):
        # 1) Si el payload trae su propio timestamp, lo parseamos; si falla, usamos ahora()
        raw_ts = values.get("timestamp")
        if raw_ts is not None:
            try:
                values["timestamp"] = parser.parse(raw_ts)
            except Exception:
                values["timestamp"] = datetime.now().astimezone()
        # 2) Deja intactos gateway_id y sensor vía alias de Pydantic
        return values

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True
        # Te permite crear instancias tanto con sensor_id como con "sensor ID"
