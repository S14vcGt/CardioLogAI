from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.patient import router as patient_router
from app.routes.medical_history import router as medical_history_router
from app.models import *
from app.core.config import engine
from sqlmodel import SQLModel

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(medical_history_router) 