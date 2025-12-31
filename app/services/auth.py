from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.models.user import User
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import verify_password
from app.services.user import UserService


class AuthService:

    def __init__(self, db_session: Session, user_service: UserService):
        self.db_session = db_session
        self.user_service = user_service
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

    def create_access_token(self,data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, username: str, password: str):
        # We use self.user_service, session not needed
        user = self.user_service.get_by_username(username)
        
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_user_from_token(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = self.user_service.get_by_username(username)
        if user is None:
            raise credentials_exception
        return user 

    def get_current_user(self, token: str = Depends(self.oauth2_scheme)) -> User:
        return self.get_user_from_token(token)  