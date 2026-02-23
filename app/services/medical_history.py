from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.models.medical_history import MedicalHistory
from app.models.patient import Patient
from app.models.user import User
from typing import List
from app.core.config import SessionDep
from app.Scripts.medical_history_helpers import calcular_edad, calcular_bsa_mosteller


def create_medical_history(
    session: SessionDep,
    patient_id: str,
    history: MedicalHistoryCreate,
    current_user: User,
):
    try:
        statement = select(Patient).where(
            Patient.id == patient_id, Patient.doctor_id == current_user.id
        )
        patient = session.exec(statement).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        history_dict = history.model_dump()
        history_dict["patient_id"] = patient_id
        history_dict["age"] = calcular_edad(patient.birth_date)  # yyyy-mm-dd
        # ?por ahora se calculara en el front el bsa
        # history_dict["body_surface_area"] = calcular_bsa_mosteller(history.weight, history.height)
        db_history = MedicalHistory(**history_dict)

        session.add(db_history)
        session.commit()
        session.refresh(db_history)
        return db_history
    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


def get_medical_histories_by_patient(
    session: SessionDep, patient_id: str, current_user: User
):
    try:
        statement = select(Patient).where(
            Patient.id == patient_id, Patient.owner_id == current_user.id
        )
        patient: Patient = session.exec(statement).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        statement = select(MedicalHistory).where(
            MedicalHistory.patient_id == patient_id
        )
        return session.exec(statement).all()
        # return patient.medical_histories
        #!probar si esto funciona
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
