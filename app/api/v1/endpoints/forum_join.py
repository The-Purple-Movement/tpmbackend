from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.forum_join import ForumJoinCreate, ForumJoinResponse
from app.services.forum_join_service import submit_forum_join

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=ForumJoinResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Forum Join Registration",
    description="Submit a registration for the AI+Compassion Global Forum"
)
def create_forum_join(data: ForumJoinCreate, db: Session = Depends(get_db)):
    return submit_forum_join(db, data)
