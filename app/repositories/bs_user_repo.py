from sqlalchemy.orm import Session
from app.models.bs_user import BSUser


def get_user_by_email(db: Session, email: str) -> BSUser | None:
    return db.query(BSUser).filter(BSUser.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> BSUser | None:
    return db.query(BSUser).filter(BSUser.id == user_id).first()


def create_user(db: Session, user_data: dict) -> BSUser:
    user = BSUser(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: BSUser, updates: dict) -> BSUser:
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
