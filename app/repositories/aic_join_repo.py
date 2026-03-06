from sqlalchemy.orm import Session
from app.models.aic_join import AICJoin


def create_aic_join(db: Session, data):
    obj = AICJoin(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_by_email(db: Session, email: str):
    return db.query(AICJoin).filter(AICJoin.email == email).first()
