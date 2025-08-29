from fastapi import APIRouter, Depends, HTTPException, status, exceptions
from typing import List
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.core.auth import get_password_hash, get_current_user, get_user_by_username
from app.services.dependencies import get_user_service
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        # db_user = get_user_by_username(session, user.username)
        # if db_user:
        # raise HTTPException(status_code=400, detail="El usuario ya existe")

        new_user = user_service.create(user)
        return new_user
    except exceptions.ResponseValidationError as e:
        return e


@router.post("/admin", response_model=UserRead)
def create_admin(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        new_user = user_service.create(user, is_admin=True)
        return new_user

    except exceptions.ResponseValidationError as e:
        return e


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{id}", response_model=UserRead)
def read_user_by_id(id: str, user_service: UserService = Depends(get_user_service)):
    return user_service.read_by_id(id)


@router.get("/", response_model=List[UserRead])
def read_all_users(user_service: UserService = Depends(get_user_service)):
    return user_service.read_all()
