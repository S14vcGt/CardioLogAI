from fastapi import APIRouter, Depends, HTTPException
from app.schemas.patient import PatientCreate, PatientRead
from app.models.patient import Patient
from app.models.user import User
from app.services.patient import create, get_all_by_doctor, get_by_id
from app.services.auth import get_current_user
from app.core.config import SessionDep
from app.core.logger import get_logger
from typing import List

logger = get_logger(__name__)

router = APIRouter(
    prefix="/patients", tags=["patients"], dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=PatientRead)
def create_patient(
    patient: PatientCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    try:
        patient.doctor_id = current_user.id
        db_patient = create(session, patient)
        return db_patient
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"Error en POST /patients/: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/", response_model=List[PatientRead])
def get_patients(session: SessionDep, current_user: User = Depends(get_current_user)):
    try:
        return get_all_by_doctor(session, doctor_id=current_user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"Error en GET /patients/: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
