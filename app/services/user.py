from sqlmodel import select
from typing import List
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash
import uuid


class UserService:

    def __init__(self, db_session):
        self.session = db_session

    def create(self, user: UserCreate, is_admin=False):

        hashed_password = get_password_hash(user.password)
        db_user = User(
            id=str(uuid.uuid4()),
            is_admin=is_admin,
            username=user.username,
            hashed_password=hashed_password,
            full_name=user.full_name,
            email=user.email,
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

    def read_by_id(self, id: str) -> User:
        statement = select(User).where(User.id == id)
        return self.session.exec(statement).first()

    def read_all(self) -> List[User]:
        result = self.session.exec(select(User)).all()
        return result

    def get_by_username(self, username: str) -> User:
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()
