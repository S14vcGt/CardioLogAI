import os
from fastapi import FastAPI
from logging import INFO, basicConfig, getLogger
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.patient import router as patient_router
from app.routes.medical_history import router as medical_history_router
from app.models import *
from app.core.config import engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from app.core.config import init_db, get_session
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")


logger = getLogger(__name__)
basicConfig(level=INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    init_db()
    yield
    logger.info("Shutting down...")
    logger.info("Finished shutting down.")


app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(medical_history_router)
