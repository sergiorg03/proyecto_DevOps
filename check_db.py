from app.database import SessionLocal
from app.models import Zone, Scooter

db = SessionLocal()
zones = db.query(Zone).all()
scooters = db.query(Scooter).all()

print(f"Zonas encontradas: {len(zones)}")
for z in zones:
    print(f"- {z.nombre} (CP: {z.codigo_postal})")

print(f"\nPatinetes encontrados: {len(scooters)}")
for s in scooters:
    print(f"- {s.numero_serie}: {s.modelo} ({s.estado.value}) - Zona ID: {s.zona_id}")

db.close()
