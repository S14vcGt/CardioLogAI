from sqlmodel import select, Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from typing import List

class PatientService:
    def __init__(self, db_session: Session):
        self.session = db_session

    def create(self, patient: PatientCreate, doctor_id: str) -> Patient:
        # Fixed: using doctor_id instead of owner_id as per model definition
        db_patient = Patient(**patient.dict(), doctor_id=doctor_id)
        self.session.add(db_patient)
        self.session.commit()
        self.session.refresh(db_patient)
        return db_patient

    def get_all_by_doctor(self, doctor_id: str) -> List[Patient]:
        statement = select(Patient).where(Patient.doctor_id == doctor_id)
        return self.session.exec(statement).all()

    def get_by_id(self, patient_id: str) -> Patient | None:
        statement = select(Patient).where(Patient.id == patient_id)
        return self.session.exec(statement).first()
