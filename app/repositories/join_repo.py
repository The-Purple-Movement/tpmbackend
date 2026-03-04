from sqlalchemy.orm import Session
from app.models.join import Join
from app.schemas.join import JoinCreate


def create_join_request(db: Session, data: JoinCreate) -> Join:
    obj = Join(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj