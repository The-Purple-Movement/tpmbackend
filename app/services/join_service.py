from sqlalchemy.orm import Session
from app.repositories.join_repo import create_join_request
from app.schemas.join import JoinCreate


def submit_join(db: Session, data: JoinCreate):
    return create_join_request(db, data)