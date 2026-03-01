from fastapi import HTTPException
from sqlalchemy.orm import Session
# from app import models
from . import models, schemas
from datetime import date

ESTADOS = ["disponible", "en_uso", "mantenimiento", "sin_bateria"]

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

def create_zone(db: Session, zone: schemas.ZoneCreate):
    """
    Función que crea una nueva zona en la base de datos.
    """
    db_zone = models.Zone(**zone.model_dump())

    if not db_zone:
        raise HTTPException(status_code=400, detail="Datos no válidos")

    if db_zone.limite_velocidad < 0:
        raise HTTPException(status_code=400, detail="El límite de velocidad no puede ser negativo")
    
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

def delete_zone(db: Session, id: int):
    zona = db.query(models.Zone).filter(models.Zone.id == id).first()

    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    
    db.delete(zona)
    db.commit()
    return {"msg": "Zona eliminada"}

'''
    Scooters
'''
def create_scooter(db: Session, scooter: schemas.ScooterCreate):
    """
    Función que crea un nuevo patinete en la base de datos.
    """
    db_scooter = models.Scooter(**scooter.model_dump())
    zona = db.query(models.Zone).filter(models.Zone.id == db_scooter.zona_id).first()

    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    if db_scooter.bateria < 0 or db_scooter.bateria > 100:
        raise HTTPException(status_code=422, detail="La batería debe estar entre 0 y 100")

    if db_scooter.estado.lower() not in ESTADOS:
        raise HTTPException(status_code=422, detail="El estado no es válido")

    try:
        db.add(db_scooter)
        db.commit()
        db.refresh(db_scooter)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="El número de serie ya existe")
    
    return db_scooter

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

def delete_scooter(db: Session, id: int):
    patinete = db.query(models.Scooter).filter(models.Scooter.id == id).first()

    if not patinete:
        raise HTTPException(status_code=404, detail="Patinete no encontrado")
    
    db.delete(patinete)
    db.commit()
    return {"msg": "Patinete eliminado"}

def auto_maintenance(db: Session, zona_id: int):
    """
    Pone en mantenimiento a todos los patinetes de una zona con batería < 15%.
    """
    # Verificamos si la zona existe
    zona = db.query(models.Zone).filter(models.Zone.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    # Buscamos los patinetes que cumplen la condición
    patinetes = db.query(models.Scooter).filter(
        models.Scooter.zona_id == zona_id,
        models.Scooter.bateria < 15
    ).all()

    for p in patinetes:
        p.estado = models.ScooterStatus.mantenimiento
    
    db.commit()
    return {"msg": f"Se han puesto {len(patinetes)} patinetes en mantenimiento"}
