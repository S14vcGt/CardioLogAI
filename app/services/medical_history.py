
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.models.medical_history import MedicalHistory
from app.models.patient import Patient
from app.models.user import User
from typing import List
from app.core.config import SessionDep

def create_medical_history(session:SessionDep, patient_id: int, history: MedicalHistoryCreate, current_user: User):
    statement = select(Patient).where(Patient.id == patient_id, Patient.doctor_id == current_user.id)
    patient = session.exec(statement).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db_history = MedicalHistory(patient_id=patient_id, description=history.description)
    session.add(db_history)
    session.commit()
    session.refresh(db_history)
    return db_history

def get_medical_histories_by_patient(session:SessionDep, patient_id: int, current_user: User):
    statement = select(Patient).where(Patient.id == patient_id, Patient.owner_id == current_user.id)
    patient = session.exec(statement).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    statement = select(MedicalHistory).where(MedicalHistory.patient_id == patient_id)
    return session.exec(statement).all() 