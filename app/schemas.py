from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional
from enum import Enum

class ScooterStatus(str, Enum):
    disponible = "disponible"
    en_uso = "en_uso"
    mantenimiento = "mantenimiento"
    sin_bateria = "sin_bateria"

class ScooterBase(BaseModel):
    numero_serie: str
    modelo: str
    #bateria: int = Field(default=100, ge=0, le=100) Correccion del error en el test 'test_create_scooter_invalid_battery' por cadena de devolucion
    bateria: int = Field(default=100)
    estado: ScooterStatus = ScooterStatus.disponible
    zona_id: Optional[int] = None

    @field_validator("bateria")
    @classmethod
    def validar_bateria(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("batería debe estar entre 0 y 100")
        return v

class ScooterCreate(ScooterBase):
    pass

class ScooterResponse(ScooterBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ZoneBase(BaseModel):
    nombre: str = "Sin nombre"
    codigo_postal: int
    limite_velocidad: int = 0

class ZoneCreate(ZoneBase):
    pass

class ZoneResponse(ZoneBase):
    id: int
    scooters: List[ScooterResponse] = []
    model_config = ConfigDict(from_attributes=True)
