import enum
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base

class ScooterStatus(enum.Enum):
    disponible = "disponible"
    en_uso = "en_uso"
    mantenimiento = "mantenimiento"
    sin_bateria = "sin_bateria"

class Zone(Base):
    __tablename__ = "zone"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, default="Sin nombre")
    codigo_postal = Column(Integer, nullable=False)
    limite_velocidad = Column(Integer, nullable=False, default=0)
    
    scooters = relationship("Scooter", back_populates="zona")

class Scooter (Base):
    __tablename__ = "scooter"

    id = Column(Integer, primary_key=True)
    numero_serie = Column(String, nullable=False, unique=True)
    modelo = Column(String, nullable=False)
    bateria = Column(Integer, nullable=False, default=100)
    estado = Column(Enum(ScooterStatus), nullable=False, default=ScooterStatus.disponible)

    zona_id = Column(Integer, ForeignKey("zone.id"))
    zona = relationship("Zone", back_populates="scooters")
