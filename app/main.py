from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
'''from app import schemas, crud
from app.deps import get_db
from app.database import Base, engine'''
from . import schemas, crud
from .deps import get_db
from .database import Base, engine

# Las tablas se gestionarán a través de migraciones con Alembic.

app = FastAPI(title="ScooterFlow API")

# Mensaje de root
@app.get("/")
def root():
    return {"msg": "API funcionando"}


'''
    Zonas
'''

@app.get("/zones/")
def get_zones(db: Session = Depends(get_db)):
    return crud.get_zones(db)

@app.get("/zones/{id}")
def get_zones_id(db: Session = Depends(get_db), id: int = -1):
    return crud.get_zones_id(db=db, id=id)

@app.post("/zones/", response_model=schemas.ZoneResponse)
def add_new_zones(zone: schemas.ZoneCreate, db: Session = Depends(get_db)):
    return crud.create_zone(db, zone)

@app.delete("/zones/{id}")
def delete_zone(db: Session = Depends(get_db), id: int = -1):
    return crud.delete_zone(db, id)

'''
    Patinetes
'''
@app.get("/scooters/")
def get_scooters(db: Session = Depends(get_db)):
    return crud.get_scooters(db)

@app.get("/scooters/{id}")
def get_scooters_id(db: Session = Depends(get_db), id: int = -1):
    return crud.get_scooters_id(db=db, id=id)

@app.post("/scooters/", response_model=schemas.ScooterResponse)
def add_new_scooter(scooter: schemas.ScooterCreate, db: Session = Depends(get_db)):
    return crud.create_scooter(db, scooter)

@app.delete("/scooters/{id}")
def delete_scooter(db: Session = Depends(get_db), id: int = -1):
    return crud.delete_scooter(db, id)