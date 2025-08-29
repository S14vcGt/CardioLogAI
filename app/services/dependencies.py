from fastapi import Depends
from app.core.config import get_session
from app.services.user import UserService

def get_user_service(db_session=Depends(get_session)) -> UserService:
    return UserService(db_session)