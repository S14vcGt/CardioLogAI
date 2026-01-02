from sqlmodel import select, Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from typing import List
from app.core.config import SessionDep



def create(session:SessionDep, patient: PatientCreate, doctor_id: str) -> Patient:
    # Fixed: using doctor_id instead of owner_id as per model definition
    db_patient = Patient(**patient.dict(), doctor_id=doctor_id)
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)
    return db_patient

def get_all_by_doctor(session:SessionDep, doctor_id: str) -> List[Patient]:
    statement = select(Patient).where(Patient.doctor_id == doctor_id)
    return session.exec(statement).all()

def get_by_id(session:SessionDep, patient_id: str) -> Patient | None:
    statement = select(Patient).where(Patient.id == patient_id)
    return session.exec(statement).first()
