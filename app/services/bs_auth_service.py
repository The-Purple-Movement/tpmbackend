import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.bs_user import (
    UserRegister, UserLogin, ChangePasswordRequest, UserProfileUpdate
)
import app.repositories.bs_user_repo as bs_user_repo
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


# helper function to generate access and refresh tokens
def _build_tokens(user_id: str) -> dict:
    token_data = {"sub": user_id}
    return {
        "access_token": create_access_token(token_data, ACCESS_TOKEN_EXPIRE_MINUTES),
        "refresh_token": create_refresh_token(token_data, REFRESH_TOKEN_EXPIRE_DAYS),
        "token_type": "bearer",
    }


def register_user(db: Session, data: UserRegister) -> dict:
    existing = bs_user_repo.get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = bs_user_repo.create_user(db, {
        "id": str(uuid.uuid4()),
        "email": data.email,
        "password_hash": hash_password(data.password),
        "full_name": data.full_name,
        "is_active": True,
    })
    return _build_tokens(user.id)


def login_user(db: Session, data: UserLogin) -> dict:
    user = bs_user_repo.get_user_by_email(db, data.email.strip().lower())
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )
    return _build_tokens(user.id)


def refresh_tokens(db: Session, refresh_token: str) -> dict:
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = bs_user_repo.get_user_by_id(db, payload.get("sub"))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    return _build_tokens(user.id)


def update_profile(db: Session, user, data: UserProfileUpdate):
    updates = {}
    if data.full_name is not None:
        updates["full_name"] = data.full_name
    if not updates:
        return user
    return bs_user_repo.update_user(db, user, updates)


def change_password(db: Session, user, data: ChangePasswordRequest):
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    bs_user_repo.update_user(db, user, {
        "password_hash": hash_password(data.new_password),
    })
    return {"message": "Password changed successfully"}
