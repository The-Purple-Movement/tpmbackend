from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.schemas.bs_user import (
    UserRegister, UserLogin, TokenResponse,
    RefreshTokenRequest, UserProfile, UserProfileUpdate,
    ChangePasswordRequest,
)
from app.services.bs_auth_service import (
    register_user, login_user, refresh_tokens,
    update_profile, change_password,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with email and password",
)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, data)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
)
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_tokens(db, data.refresh_token)


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Get current user profile",
)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.put(
    "/me",
    response_model=UserProfile,
    summary="Update current user profile",
)
def update_me(
    data: UserProfileUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_profile(db, current_user, data)


@router.post(
    "/change-password",
    summary="Change password",
)
def change_pwd(
    data: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return change_password(db, current_user, data)
