from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.medical_history import MedicalHistoryCreate
from app.models.user import User
from app.core.logger import get_logger
from app.services.auth import get_current_user
from app.services.model.predict import predict_heart_disease

logger = get_logger(__name__)

router = APIRouter(
    prefix="/model",
    tags=["model"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/predict")
def predict(
    data: MedicalHistoryCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """Usa el modelo de IA para predecir enfermedad cardíaca."""
    try:
        model = request.state.model
        result = predict_heart_disease(data, model)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"Error en POST /model/predict: {e}")
        raise e
