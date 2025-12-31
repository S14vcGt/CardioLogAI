from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.models.medical_history import MedicalHistory
from app.models.patient import Patient
from app.models.user import User
from app.core.config import get_session
from app.services.dependencies import get_current_user
from typing import List
from app.services.dependencies import get_current_user, get_medical_history_service
from app.services.medical_history import MedicalHistoryService

router = APIRouter(prefix="/patients/{patient_id}/histories", tags=["medical_histories"])

@router.post("/", response_model=MedicalHistoryRead)
def create_mh(
    patient_id: int, 
    history: MedicalHistoryCreate, 
    service: MedicalHistoryService = Depends(get_medical_history_service),
    current_user: User = Depends(get_current_user)
):
    result = service.create_medical_history(patient_id, history, current_user)
    return result

@router.get("/", response_model=List[MedicalHistoryRead])
def get_mh(
    patient_id: int, 
    service: MedicalHistoryService = Depends(get_medical_history_service),
    current_user: User = Depends(get_current_user)
):
   result =  service.get_medical_histories(patient_id, current_user)
   return result