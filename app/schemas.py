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
            raise ValueError("La bateria debe estar entre 0 y 100")
        return v

class ScooterCreate(ScooterBase):
    numero_serie: str
    bateria: int
    zona_id: int
    estado: ScooterStatus

    @field_validator("estado", mode="before")
    @classmethod
    def normalize_estado(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

class ScooterUpdate(BaseModel):
    numero_serie: Optional[str] = None
    modelo: Optional[str] = None
    bateria: Optional[int] = None
    estado: Optional[ScooterStatus] = None
    zona_id: Optional[int] = None
    puntuacion_usuario: Optional[float] = None

    @field_validator("bateria")
    @classmethod
    def validar_bateria(cls, v):
        if v is not None and not 0 <= v <= 100:
            raise ValueError("La bateria debe estar entre 0 y 100")
        return v

    @field_validator("puntuacion_usuario")
    @classmethod
    def validar_puntuacion(cls, v):
        if v is not None and not 0 <= v <= 5:
            raise ValueError("puntuacion debe estar entre 0 y 5")
        return v

    @field_validator("estado", mode="before")
    @classmethod
    def normalize_estado(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

class ScooterResponse(ScooterBase):
    id: int
    puntuacion_usuario: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class ZoneBase(BaseModel):
    nombre: str = "Sin nombre"
    codigo_postal: int
    limite_velocidad: int = 0

class ZoneCreate(ZoneBase):
    pass

class ZoneUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo_postal: Optional[int] = None
    limite_velocidad: Optional[int] = None

    @field_validator("limite_velocidad")
    @classmethod
    def validar_limite_velocidad(cls, v):
        if v is not None and v < 0:
            raise ValueError("El limite de velocidad no puede ser negativo")
        return v

    @field_validator("codigo_postal")
    @classmethod
    def validar_codigo_postal(cls, v):
        if v is None:
            raise ValueError("Debe introducir un valor para el codigo postal valido")
        elif v < 0:
            raise ValueError("El codigo postal no puede ser negativo")
        return v

class ZoneResponse(ZoneBase):
    id: int
    scooters: List[ScooterResponse] = []
    model_config = ConfigDict(from_attributes=True)

