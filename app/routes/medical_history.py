from fastapi import APIRouter, Depends, HTTPException
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.models.medical_history import MedicalHistory
from app.models.patient import Patient
from app.models.user import User
from app.core.config import SessionDep
from app.services.auth import get_current_user
from typing import List
from app.services.medical_history import (
    create_medical_history,
    get_medical_histories_by_patient,
)

router = APIRouter(
    prefix="/patients/{patient_id}/histories", tags=["medical_histories"]
)


@router.post("/", response_model=MedicalHistoryRead)
def create_mh(
    patient_id: str,
    history: MedicalHistoryCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    try:
        result = create_medical_history(session, patient_id, history, current_user)
        return result
    except Exception as e:
        raise e


@router.get("/", response_model=List[MedicalHistoryRead])
def get_mh(
    patient_id: str, session: SessionDep, current_user: User = Depends(get_current_user)
):
    try:
        result = get_medical_histories_by_patient(session, patient_id, current_user)
        return result
    except Exception as e:
        raise e
