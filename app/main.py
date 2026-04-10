import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.logger import get_logger, setup_db_logger
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.patient import router as patient_router
from app.routes.medical_history import router as medical_history_router
from app.routes.model import router as model_router
from app.models import *
from contextlib import asynccontextmanager
from app.core.config import init_db
from dotenv import load_dotenv
import joblib


load_dotenv(dotenv_path="../.env")

logger = get_logger(__name__)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://cardiologai.vercel.app",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    setup_db_logger()
    if not os.getenv("TESTING"):
        init_db()
        model = joblib.load("./app/services/model/heart_disease_pipeline_v1.pkl")
        logger.info("Modelo cargado exitosamente.")
        preprocessor = joblib.load('./app/services/model/preprocessor.joblib')
        logger.info("Preprocessor cargado exitosamente.")

    yield {"model": model, "preprocessor": preprocessor}

    logger.info("Shutting down...")

    logger.info("Liberando modelo de la memoria...")
    model = None

    logger.info("Finished shutting down.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Loguea errores HTTP y los propaga con CORS headers."""
    logger.warning(
        f"HTTP {exc.status_code} en {request.method} {request.url.path}: {exc.detail}"
    )
    origin = request.headers.get("origin")
    headers = {}
    if origin in ALLOWED_ORIGINS:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=headers,
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all: loguea excepciones no manejadas con traceback completo."""
    logger.exception(f"Error no manejado en {request.method} {request.url.path}: {exc}")
    origin = request.headers.get("origin")
    headers = {}
    if origin in ALLOWED_ORIGINS:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"},
        headers=headers,
    )


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(medical_history_router)
app.include_router(model_router)
