from fastapi import HTTPException
from sqlalchemy.orm import Session
# from app import models
from . import models
from datetime import date

'''
    Zones
'''
def get_zones(db: Session):
    """
        Función que obtiene todas las zonas existentes en la base de datos.
    """
    return db.query(models.Zone).all()

def get_zones_id(db: Session, id: int):
    """
        Función que obtiene la zona con el id indicado.
    """
    return db.query(models.Zone).filter(models.Zone.id == id).first()

'''
    Scooters
'''
def get_scooters(db: Session):
    return db.query(models.Scooter).all()