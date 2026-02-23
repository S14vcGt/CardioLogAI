from sqlmodel import select, Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from typing import Sequence
from app.core.config import SessionDep
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import uuid

def create(session:SessionDep, patient: PatientCreate) -> Patient:
    try:
        db_patient = Patient(**patient.model_dump())
        session.add(db_patient)
        session.commit()
        session.refresh(db_patient)
        return db_patient
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Cedula ya registrada")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


def get_all_by_doctor(session:SessionDep, doctor_id: str) -> Sequence[Patient]:
    try: 
        statement = select(Patient).where(Patient.doctor_id == doctor_id)
        return session.exec(statement).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_by_id(session:SessionDep, patient_id: str) -> Patient | None:
    try:
        statement = select(Patient).where(Patient.id == patient_id)
        patient = session.exec(statement).first()

        if not patient:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        return patient
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")



'''def edit_patient(session:SessionDep, patient: Patient) -> Patient:
'''


