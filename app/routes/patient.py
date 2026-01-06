
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.patient import PatientCreate, PatientRead
from app.models.patient import Patient
from app.models.user import User
from app.services.patient import create, get_all_by_doctor
from app.services.auth import get_current_user
from app.core.config import SessionDep
from typing import List

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientRead)
def create_patient(
    patient: PatientCreate, 
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    # Service expects doctor_id, we use current_user.id
    db_patient = create(session, patient, doctor_id=current_user.id)
    return db_patient

@router.get("/", response_model=List[PatientRead])
def get_patients(
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    return get_all_by_doctor(session, doctor_id=current_user.id) 