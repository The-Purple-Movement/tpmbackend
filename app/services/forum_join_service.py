from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repositories.forum_join_repo import create_forum_join, get_by_email


def submit_forum_join(db, data):
    existing = get_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already registered"
        )

    try:
        return create_forum_join(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already registered"
        )
