from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.aic_join import AICJoinCreate, AICJoinResponse
from app.services.aic_join_service import submit_aic_join

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=AICJoinResponse,
    status_code=status.HTTP_201_CREATED,
    summary="AI+C Join Registration",
    description="Submit a registration for the AI+Compassion Global Forum"
)
def create_aic_join(data: AICJoinCreate, db: Session = Depends(get_db)):
    return submit_aic_join(db, data)
