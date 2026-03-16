import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from pydantic import ValidationError
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead
from app.services.medical_history import (
    create_medical_history,
    get_medical_histories_by_patient,
)
from app.models.patient import Patient
from app.models.user import User


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_user():
    return User(
        id="user-123",
        email="doctor@test.com",
        password="hashed_password",
        first_name="Doc",
        last_name="Tor",
    )


@pytest.fixture
def mock_patient():
    p = MagicMock(spec=Patient)
    p.id = "patient-123"
    p.doctor_id = "user-123"
    p.birth_date = "1990-01-01"
    p.owner_id = "user-123"
    return p


@pytest.fixture
def valid_history_data():
    """Datos válidos reutilizables para crear historia médica."""
    return MedicalHistoryCreate(
        smoking_status="never",
        sedentary_lifestyle=False,
        blood_pressure=120,
        ldl_cholesterol=100,
        max_hr=150.0,
        fasting_blood_sugar=90,
        body_mass_index=22.0,
        rest_ecg="normal",
        height=175,
        weight=70,
        body_surface_area=1.85,
        description="Routine check",
        heart_disease=False,
    )


# ============================================================
# Tests del Servicio – create_medical_history
# ============================================================


class TestCreateMedicalHistory:

    @patch("app.services.medical_history.calcular_edad")
    def test_success(
        self, mock_calc_edad, mock_session, mock_user, mock_patient, valid_history_data
    ):
        """Creación exitosa de historia médica."""
        patient_id = "patient-123"

        mock_exec = MagicMock()
        mock_exec.first.return_value = mock_patient
        mock_session.exec.return_value = mock_exec
        mock_calc_edad.return_value = 33

        result = create_medical_history(
            mock_session, patient_id, valid_history_data, mock_user
        )

        assert result.patient_id == patient_id
        assert result.age == 33
        assert result.smoking_status == "never"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_patient_not_found(self, mock_session, mock_user, valid_history_data):
        """Error 404 cuando el paciente no existe."""
        mock_exec = MagicMock()
        mock_exec.first.return_value = None
        mock_session.exec.return_value = mock_exec

        with pytest.raises(HTTPException) as exc:
            create_medical_history(
                mock_session, "patient-unknown", valid_history_data, mock_user
            )

        assert exc.value.status_code == 404
        assert "Paciente no encontrado" in exc.value.detail
        mock_session.add.assert_not_called()

    @patch("app.services.medical_history.calcular_edad")
    def test_db_error(
        self, mock_calc_edad, mock_session, mock_user, mock_patient, valid_history_data
    ):
        """Error 500 cuando falla la base de datos al hacer commit."""
        mock_exec = MagicMock()
        mock_exec.first.return_value = mock_patient
        mock_session.exec.return_value = mock_exec
        mock_calc_edad.return_value = 33
        mock_session.commit.side_effect = Exception("DB Connection Failed")

        with pytest.raises(HTTPException) as exc:
            create_medical_history(
                mock_session, "patient-123", valid_history_data, mock_user
            )

        assert exc.value.status_code == 500
        mock_session.rollback.assert_called_once()

    def test_unauthorized_doctor(self, mock_session, valid_history_data):
        """Un doctor que no es dueño del paciente recibe 404 (el query no lo encuentra)."""
        other_user = User(
            id="user-OTHER",
            email="other@test.com",
            password="hashed",
            first_name="Other",
            last_name="Doc",
        )

        # El query filtra por doctor_id == current_user.id, así que no encuentra nada
        mock_exec = MagicMock()
        mock_exec.first.return_value = None
        mock_session.exec.return_value = mock_exec

        with pytest.raises(HTTPException) as exc:
            create_medical_history(
                mock_session, "patient-123", valid_history_data, other_user
            )

        assert exc.value.status_code == 404
        mock_session.add.assert_not_called()


# ============================================================
# Tests del Servicio – get_medical_histories_by_patient
# ============================================================


class TestGetMedicalHistories:

    def test_success(self, mock_session, mock_user, mock_patient):
        """Retorna lista de historias cuando el paciente existe."""
        mock_exec_patient = MagicMock()
        mock_exec_patient.first.return_value = mock_patient

        mock_histories_list = [MagicMock(id="hist-1"), MagicMock(id="hist-2")]
        mock_exec_histories = MagicMock()
        mock_exec_histories.all.return_value = mock_histories_list

        mock_session.exec.side_effect = [mock_exec_patient, mock_exec_histories]

        result = get_medical_histories_by_patient(
            mock_session, "patient-123", mock_user
        )

        assert len(result) == 2
        assert result[0].id == "hist-1"

    def test_patient_not_found(self, mock_session, mock_user):
        """Error 404 cuando el paciente no existe."""
        mock_exec = MagicMock()
        mock_exec.first.return_value = None
        mock_session.exec.return_value = mock_exec

        with pytest.raises(HTTPException) as exc:
            get_medical_histories_by_patient(
                mock_session, "patient-unknown", mock_user
            )

        assert exc.value.status_code == 404

    def test_db_error(self, mock_session, mock_user):
        """Error 500 cuando falla la base de datos al consultar."""
        mock_session.exec.side_effect = Exception("Connection lost")

        with pytest.raises(HTTPException) as exc:
            get_medical_histories_by_patient(
                mock_session, "patient-123", mock_user
            )

        assert exc.value.status_code == 500


# ============================================================
# Tests del Schema – MedicalHistoryCreate
# ============================================================


class TestMedicalHistoryCreateSchema:

    def test_valid_complete(self):
        """Creación con todos los campos válidos."""
        data = {
            "smoking_status": "no smoker",
            "sedentary_lifestyle": False,
            "blood_pressure": 120,
            "ldl_cholesterol": 100,
            "max_hr": 150.0,
            "fasting_blood_sugar": 90,
            "body_mass_index": 22.5,
            "rest_ecg": "normal",
            "height": 175,
            "weight": 70,
            "body_surface_area": 1.85,
            "description": "Routine checkup",
            "heart_disease": False,
        }
        schema = MedicalHistoryCreate(**data)
        assert schema.smoking_status == "no smoker"
        assert schema.blood_pressure == 120
        assert schema.heart_disease is False

    def test_optional_fields_accept_none(self):
        """Campos opcionales aceptan None explícito."""
        data = {
            "smoking_status": "active smoker",
            "sedentary_lifestyle": True,
            "blood_pressure": 140,
            "ldl_cholesterol": 160,
            "max_hr": 170.0,
            "rest_ecg": "abnormal",
            "height": 180,
            "weight": 90,
            "fasting_blood_sugar": None,
            "body_mass_index": None,
            "body_surface_area": None,
            "description": None,
            "heart_disease": None,
        }
        schema = MedicalHistoryCreate(**data)
        assert schema.fasting_blood_sugar is None
        assert schema.body_mass_index is None
        assert schema.body_surface_area is None
        assert schema.description is None
        assert schema.heart_disease is None

    def test_missing_required_fields(self):
        """Falta de campo requerido genera ValidationError."""
        data = {
            "smoking_status": "smoker",
            # Faltan: sedentary_lifestyle, blood_pressure, ldl_cholesterol, max_hr, rest_ecg, height, weight
        }
        with pytest.raises(ValidationError):
            MedicalHistoryCreate(**data)

    def test_invalid_types(self):
        """Tipos incorrectos generan ValidationError."""
        data = {
            "smoking_status": "never",
            "sedentary_lifestyle": "not_a_bool",  # debería ser bool
            "blood_pressure": "high",  # debería ser int
            "ldl_cholesterol": 100,
            "max_hr": 150.0,
            "rest_ecg": "normal",
            "height": 175,
            "weight": 70,
        }
        with pytest.raises(ValidationError):
            MedicalHistoryCreate(**data)


# ============================================================
# Tests del Schema – MedicalHistoryRead
# ============================================================


class TestMedicalHistoryReadSchema:

    def test_serialization(self):
        """MedicalHistoryRead se instancia correctamente con todos los campos."""
        data = {
            "id": "uuid-123",
            "age": 30,
            "smoking_status": "never",
            "sedentary_lifestyle": False,
            "blood_pressure": 110,
            "ldl_cholesterol": 90,
            "max_hr": 160.0,
            "fasting_blood_sugar": 85,
            "body_mass_index": 21.0,
            "rest_ecg": "normal",
            "height": 170.0,
            "weight": 65.0,
            "body_surface_area": 1.75,
            "created_at": "2023-10-10T00:00:00",
            "description": "Clean bill of health",
            "heart_disease": False,
        }
        model = MedicalHistoryRead(**data)
        assert model.id == "uuid-123"
        assert model.age == 30
        assert model.heart_disease is False
