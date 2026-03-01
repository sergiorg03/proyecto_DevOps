import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Cargar el .env para obtener la DATABASE_URL
load_dotenv()

from app.database import Base
from app.main import app
from app.deps import get_db
from app.models import Zone, Scooter, ScooterStatus

# Usa la variable de entorno DATABASE_URL (PostgreSQL de Docker)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://scooteruser:scooterpassword@localhost:5432/scooterflow"
)

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Dependencia de BD: cada request abre y cierra su propia sesión."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Crea las tablas UNA VEZ para toda la sesión de tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def clean_and_seed():
    """Limpia y re-siembra la BD antes de cada test."""
    db = TestingSessionLocal()
    try:
        # Truncar en orden correcto (hijos primero por FK)
        db.execute(text("TRUNCATE TABLE scooter, zone RESTART IDENTITY CASCADE"))
        db.commit()

        # Seed: insertar datos iniciales
        centro = Zone(nombre="Centro Histórico", codigo_postal=28001, limite_velocidad=20)
        db.add(centro)
        db.commit()
        db.refresh(centro)

        scooter = Scooter(
            numero_serie="S001",
            modelo="Xiaomi M365",
            bateria=85,
            estado=ScooterStatus.disponible,
            zona_id=centro.id
        )
        db.add(scooter)
        db.commit()
        db.refresh(scooter)

        # IDs disponibles para los tests
        pytest.seeded_zone_id = centro.id
        pytest.seeded_scooter_id = scooter.id
    finally:
        db.close()

    yield


@pytest.fixture(scope="function")
def client():
    """TestClient que usa PostgreSQL a través del override de dependencia."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
