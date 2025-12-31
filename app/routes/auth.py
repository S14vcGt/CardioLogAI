from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.services.dependencies import get_auth_service
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    access_token_expires = timedelta(minutes=60)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"} 