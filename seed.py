from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Zone, Scooter, ScooterStatus
import traceback

def seed_data():
    # Las tablas se gestionan mediante Alembic
    
    db: Session = SessionLocal()
    try:
        # Verificar si ya hay datos para evitar duplicados
        if db.query(Zone).first():
            print("La base de datos ya tiene información. Saltando seed.")
            return

        print("Introduciendo datos iniciales...")

        # 1. Crear Zonas
        centro = Zone(nombre="Centro deresha", codigo_postal=28001, limite_velocidad=20)
        norte = Zone(nombre="Las 3k", codigo_postal=28050, limite_velocidad=30)
        retiro = Zone(nombre="Parque de los principes", codigo_postal=28009, limite_velocidad=10)

        db.add_all([centro, norte, retiro])
        db.commit() # Commit para obtener los IDs de las zonas

        # 2. Crear Patinetes
        patinetes = [
            Scooter(numero_serie="001", modelo="Chami Pro 2", bateria=85, estado=ScooterStatus.disponible, zona_id=centro.id),
            Scooter(numero_serie="002", modelo="AMR Patineta", bateria=10, estado=ScooterStatus.sin_bateria, zona_id=centro.id),
            Scooter(numero_serie="003", modelo="Lacha tarra", bateria=100, estado=ScooterStatus.en_uso, zona_id=norte.id),
            Scooter(numero_serie="004", modelo="Aquiles Bailo", bateria=50, estado=ScooterStatus.mantenimiento, zona_id=retiro.id),
            Scooter(numero_serie="005", modelo="Pato lavida", bateria=95, estado=ScooterStatus.disponible, zona_id=retiro.id),
        ]

        db.add_all(patinetes)
        db.commit()
        print("¡Información introducida con éxito!")

    except Exception as e:
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
