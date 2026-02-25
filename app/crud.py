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
    zonas = db.query(models.Zone).all()

    if not zonas:
        raise HTTPException(status_code=404, detail="No hay zonas")
    
    return zonas

def get_zones_id(db: Session, id: int):
    """
        Función que obtiene la zona con el id indicado.
    """
    zona = db.query(models.Zone).filter(models.Zone.id == id).first()

    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    
    return zona

'''
    Scooters
'''
def get_scooters(db: Session):
    '''
        Función que obtiene todos los patinetes existentes en la base de datos.
    '''
    patinetes = db.query(models.Scooter).all()

    if not patinetes:
        raise HTTPException(status_code=404, detail="No hay patinetes")
    
    return patinetes

def get_scooters_id(db: Session, id: int):
    '''
        Función que obtiene el patinete con el id indicado.
    '''
    patinete = db.query(models.Scooter).filter(models.Scooter.id == id).first()

    if not patinete:
        raise HTTPException(status_code=404, detail="Patinete no encontrado")
    
    return patinete
