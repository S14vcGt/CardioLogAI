
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.models.medical_history import MedicalHistory
from app.models.patient import Patient
from app.models.user import User
from app.core.config import get_session
from app.core.auth import get_current_user
from typing import List

def create_medical_history(patient_id: int, history: MedicalHistoryCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    statement = select(Patient).where(Patient.id == patient_id, Patient.doctor_id == current_user.id)
    patient = session.exec(statement).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db_history = MedicalHistory(patient_id=patient_id, description=history.description)
    session.add(db_history)
    session.commit()
    session.refresh(db_history)
    return db_history

def get_medical_histories(patient_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    statement = select(Patient).where(Patient.id == patient_id, Patient.owner_id == current_user.id)
    patient = session.exec(statement).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    statement = select(MedicalHistory).where(MedicalHistory.patient_id == patient_id)
    return session.exec(statement).all() 