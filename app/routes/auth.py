from fastapi import APIRouter, Depends, HTTPException
from app.core.config import SessionDep
from app.core.logger import get_logger
from fastapi.security import OAuth2PasswordRequestForm
import app.services.auth as AuthService

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def login_for_access_token(
    session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()
):

    user = AuthService.authenticate_user(
        session, form_data.username, form_data.password
    )

    if not user:
        logger.warning(f"Intento de login fallido para usuario '{form_data.username}'")
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    access_token = AuthService.create_access_token(data={"sub": user.username})
    logger.info(f"Login exitoso: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}
