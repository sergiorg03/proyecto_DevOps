from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
'''from app import schemas, crud
from app.deps import get_db
from app.database import Base, engine'''
from . import schemas, crud
from .deps import get_db
from .database import Base, engine

# Evitamos que la app falle si ocurre un error a la hora de crearse las tablas.
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error: {e}")

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

'''
    Patinetes
'''
@app.get("/scooters/")
def get_scooters(db: Session = Depends(get_db)):
    return crud.get_scooters(db)

@app.get("/scooters/{id}")
def get_scooters_id(db: Session = Depends(get_db), id: int = -1):
    return crud.get_scooters_id(db=db, id=id)