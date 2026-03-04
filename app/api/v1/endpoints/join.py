from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.join import JoinCreate, JoinResponse
from app.services.join_service import submit_join

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=JoinResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Request to Join Community",
    description=(
        "Submit a join request for the TPM community. "
        "Provide your category (individual / organisation / government), "
        "what defines you (dropdown), what you want to share, and an optional link. "
        "Toggle `is_anonymous` to stay anonymous — otherwise name, email, and phone are required."
    )
)
def create_join(data: JoinCreate, db: Session = Depends(get_db)):
    return submit_join(db, data)