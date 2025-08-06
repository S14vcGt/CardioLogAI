from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.core.config import get_session
from app.core.auth import get_password_hash, get_current_user, get_user_by_username

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = get_user_by_username(session, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, full_name=user.full_name, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user 