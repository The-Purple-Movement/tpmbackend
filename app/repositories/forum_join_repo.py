from sqlalchemy.orm import Session
from app.models.forum_join import ForumJoin


def create_forum_join(db: Session, data):
    obj = ForumJoin(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_by_email(db: Session, email: str):
    return db.query(ForumJoin).filter(ForumJoin.email == email).first()
