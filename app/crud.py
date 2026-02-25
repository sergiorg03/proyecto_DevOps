from fastapi import HTTPException
from sqlalchemy.orm import Session
# from app import models
from . import models
from datetime import date

'''
    Zones
'''
def get_zones(db: Session):
    return db.query(models.Zone).all()

'''
    Scooters
'''
def get_scooters(db: Session):
    return db.query(models.Scooter).all()