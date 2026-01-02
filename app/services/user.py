from sqlmodel import select
from typing import List
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash
import uuid
from app.core.config import SessionDep

def create(session:SessionDep, user: UserCreate, is_admin=False):

    hashed_password = get_password_hash(user.password)
    db_user = User(
        id=str(uuid.uuid4()),
        is_admin=is_admin,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

def read_by_id(session: SessionDep, id: str) -> User:
    statement = select(User).where(User.id == id)
    return session.exec(statement).first()

def read_all(session: SessionDep) -> List[User]:
    result = session.exec(select(User)).all()
    return result

def get_by_username(session: SessionDep, username: str) -> User:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()
