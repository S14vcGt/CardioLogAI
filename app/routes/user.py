from fastapi import APIRouter, Depends, HTTPException, status, exceptions
from typing import Sequence
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.services.auth import get_current_user
from app.services import user as user_service
from app.core.config import SessionDep
from typing import Annotated

router = APIRouter(
    prefix="/users", tags=["users"]
)  # , dependencies=[Depends(get_current_user)]


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: SessionDep):
    try:
        new_user = user_service.create(session, user)
        return new_user
    except exceptions.ResponseValidationError:
        raise HTTPException(400, "Bad request")
    except Exception as e:
        HTTPException(500, f"Error inesperado: {str(e)}")


@router.post("/admin", response_model=UserRead)
def create_admin(user: UserCreate, session: SessionDep):
    try:
        new_user = user_service.create(session, user, is_admin=True)
        return new_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


@router.get("/search/{id}", response_model=UserRead)
def read_user_by_id(user=Depends(user_service.read_by_id)) -> User:
    try:
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


@router.get("/", response_model=Sequence[UserRead])
def read_all_users(all_users=Depends(user_service.read_all)) -> Sequence[User]:
    try:
        return all_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


@router.get("/admin", response_model=Sequence[UserRead])
def read_all_admins(all_admins=Depends(user_service.read_all_admins)) -> Sequence[User]:
    try:
        return all_admins
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
