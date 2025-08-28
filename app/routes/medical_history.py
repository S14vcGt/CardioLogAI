from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.models.medical_history import MedicalHistory
from app.models.patient import Patient
from app.models.user import User
from app.core.config import get_session
from app.core.auth import get_current_user
from typing import List
from app.services.medical_history import create_medical_history, get_medical_histories

router = APIRouter(prefix="/patients/{patient_id}/histories", tags=["medical_histories"])

@router.post("/", response_model=MedicalHistoryRead)
def create(patient_id: str, history: MedicalHistoryCreate):
    result = create_medical_history(patient_id,history)
    return result

@router.get("/", response_model=List[MedicalHistoryRead])
def get_medical_histories(patient_id: str):
   result =  get_medical_histories(patient_id)
   return result