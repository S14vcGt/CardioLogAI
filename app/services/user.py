from sqlmodel import select
from typing import Sequence
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash
import uuid
from app.core.config import SessionDep
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


def create(session: SessionDep, user: UserCreate, is_admin=False):

    hashed_password = get_password_hash(user.password)
    db_user = User(
        id=str(uuid.uuid4()),
        is_admin=is_admin,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        email=user.email,
    )
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Usuario o Email ya registrado")
    except Exception as e:
        session.rollback()
        raise e

    return db_user


def read_by_id(session: SessionDep, id: str) -> User:
    try:
        statement = select(User).where(User.id == id, User.is_admin == False)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return user
    except Exception as e:
        raise e


def read_all(session: SessionDep) -> Sequence[User]:
    try:
        result = session.exec(select(User).where(User.is_admin == False)).all()
        return result
    except Exception as e:
        raise e


def read_all_admins(session: SessionDep) -> Sequence[User]:
    try:
        result = session.exec(select(User).where(User.is_admin == True)).all()
        return result
    except Exception as e:
        raise e


def get_by_username(session: SessionDep, username: str) -> User:
    try:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return user
    except Exception as e:
        raise e
