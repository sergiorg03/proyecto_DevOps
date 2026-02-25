from fastapi import HTTPException
from sqlalchemy.orm import Session
# from app import models
from . import models
from datetime import date

'''
    TODO: 
        - COMPROBAR DATOS INEXISTENTES.

'''


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
    '''
        Función que obtiene todos los patinetes existentes en la base de datos.
    '''
    return db.query(models.Scooter).all()

def get_scooters_id(db: Session, id: int):
    '''
        Función que obtiene el patinete con el id indicado.
    '''
    return db.query(models.Scooter).filter(models.Scooter.id == id).first()
