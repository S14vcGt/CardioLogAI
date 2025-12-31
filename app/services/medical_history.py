
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.models.medical_history import MedicalHistory
from app.models.patient import Patient
from app.models.user import User
from typing import List

class MedicalHistoryService:

    def __init__(self, db_session):
            self.session = db_session

    def create_medical_history(self, patient_id: int, history: MedicalHistoryCreate, current_user: User):
        statement = select(Patient).where(Patient.id == patient_id, Patient.doctor_id == current_user.id)
        patient = self.session.exec(statement).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        db_history = MedicalHistory(patient_id=patient_id, description=history.description)
        self.session.add(db_history)
        self.session.commit()
        self.session.refresh(db_history)
        return db_history

    def get_medical_histories_by_patient(self, patient_id: int, current_user: User):
        statement = select(Patient).where(Patient.id == patient_id, Patient.owner_id == current_user.id)
        patient = self.session.exec(statement).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        statement = select(MedicalHistory).where(MedicalHistory.patient_id == patient_id)
        return self.session.exec(statement).all() 