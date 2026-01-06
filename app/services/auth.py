from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.models.user import User
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, get_session
from app.core.security import verify_password
from app.core.config import SessionDep 
from app.services.user import get_by_username
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(session: SessionDep, username: str, password: str):
    user = get_by_username(session, username)
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_user_from_token(session: SessionDep, token: str):
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
    
    user = get_by_username(session, username)

    if user is None:
        raise credentials_exception
    return user 

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
    return get_user_from_token(session, token)