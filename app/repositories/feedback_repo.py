from sqlalchemy.orm import Session
from app.models.feedback import Feedback

def create_feedback(db: Session, data):
    obj = Feedback(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj