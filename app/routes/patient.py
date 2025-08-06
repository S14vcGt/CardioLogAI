from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.patient import PatientCreate, PatientRead
from app.models.patient import Patient
from app.models.user import User
from app.core.config import get_session
from app.core.auth import get_current_user
from typing import List

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientRead)
def create_patient(patient: PatientCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_patient = Patient(**patient.dict(), owner_id=current_user.id)
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[PatientRead])
def get_patients(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    statement = select(Patient).where(Patient.owner_id == current_user.id)
    return session.exec(statement).all() 