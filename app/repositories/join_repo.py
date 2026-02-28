from sqlalchemy.orm import Session
from app.models.join import Join

def create_join_request(db: Session, data):
    obj = Join(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj