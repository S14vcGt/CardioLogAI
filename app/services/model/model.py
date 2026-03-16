from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.models.medical_history import MedicalHistory
from app.models.patient import Patient
from app.models.user import User
from app.core.config import SessionDep
from app.core.logger import get_logger

logger = get_logger(__name__)

def model_predict():
    pass
