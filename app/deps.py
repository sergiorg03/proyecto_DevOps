from .database import SessionLocal

# Dependencia de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()