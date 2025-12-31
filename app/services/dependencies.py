from fastapi import Depends
from app.core.config import get_session
from app.services.user import UserService
from app.services.medical_history import MedicalHistoryService
from app.services.patient import PatientService
from app.services.auth import AuthService

def get_user_service(db_session=Depends(get_session)) -> UserService:
    return UserService(db_session)

def get_medical_history_service(db_session=Depends(get_session)) -> MedicalHistoryService:
    return MedicalHistoryService(db_session)

def get_patient_service(db_session=Depends(get_session)) -> PatientService:
    return PatientService(db_session)

def get_auth_service(
    db_session=Depends(get_session), 
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    return AuthService(db_session, user_service)