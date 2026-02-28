from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import submit_feedback

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Website Feedback",
    description="Allows users to submit feedback about the community website"
)
def create_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    return submit_feedback(db, data)