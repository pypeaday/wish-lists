from app.database.database import SessionLocal, engine
from app.model import model

model.Base.metadata.create_all(bind=engine)


def create_get_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
