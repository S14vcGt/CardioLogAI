
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.patient import PatientCreate, PatientRead
from app.models.patient import Patient
from app.models.user import User
from app.services.patient import PatientService
from app.services.auth import get_current_user
from typing import List

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientRead)
def create_patient(
    patient: PatientCreate, 
    service: PatientService = Depends(PatientService), 
    current_user: User = Depends(get_current_user)
):
    # Service expects doctor_id, we use current_user.id
    db_patient = service.create(patient, doctor_id=current_user.id)
    return db_patient

@router.get("/", response_model=List[PatientRead])
def get_patients(
    service: PatientService = Depends(PatientService), 
    current_user: User = Depends(get_current_user)
):
    return service.get_all_by_doctor(doctor_id=current_user.id) 