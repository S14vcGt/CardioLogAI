import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.services.medical_history import (
    create_medical_history,
    get_medical_histories_by_patient,
)
from app.models.patient import Patient
from app.models.user import User
from app.schemas.medical_history import MedicalHistoryCreate


class TestMedicalHistoryService:

    @pytest.fixture
    def mock_session(self):
        return MagicMock()

    @pytest.fixture
    def mock_user(self):
        return User(
            id="user-123",
            email="doctor@test.com",
            password="hashed_password",
            first_name="Doc",
            last_name="Tor",
        )

    @pytest.fixture
    def mock_patient(self):
        # Patient implementation might require more fields, but for mocking return value usually simple object works
        # providing it has attributes accessed.
        # However, SQLModel objects are Pydantic models.
        # We can simulate minimal attributes: id, doctor_id, birth_date='1990-01-01'
        p = MagicMock(spec=Patient)
        p.id = "patient-123"
        p.doctor_id = "user-123"
        p.birth_date = "1990-01-01"
        p.owner_id = "user-123"  # For get_medical_histories check
        return p

    @patch("app.services.medical_history.calcular_edad")
    def test_create_medical_history_success(
        self, mock_calc_edad, mock_session, mock_user, mock_patient
    ):
        # Arrange
        patient_id = "patient-123"
        history_data = MedicalHistoryCreate(
            smoking_status="never",
            sedentary_lifestyle=False,
            blood_pressure=120,
            ldl_cholesterol=100,
            fasting_blood_sugar=90,
            body_mass_index=22.0,
            recg="normal",
            height=175,
            weight=70,
            body_surface_area=1.85,
            description="Routine check",
            diabetes=False,
        )

        # Mocking the select query result
        # session.exec(statement).first() returns mock_patient
        mock_exec = MagicMock()
        mock_exec.first.return_value = mock_patient
        mock_session.exec.return_value = mock_exec

        mock_calc_edad.return_value = 33  # Mocked age

        # Act
        result = create_medical_history(
            mock_session, patient_id, history_data, mock_user
        )

        # Assert
        assert result.patient_id == patient_id
        assert result.age == 33
        assert result.smoking_status == "never"

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_create_medical_history_patient_not_found(self, mock_session, mock_user):
        # Arrange
        patient_id = "patient-unknown"
        history_data = MedicalHistoryCreate(
            smoking_status="never",
            sedentary_lifestyle=False,
            blood_pressure=120,
            ldl_cholesterol=100,
            fasting_blood_sugar=90,
            body_mass_index=22.0,
            recg="normal",
            height=175,
            weight=70,
            body_surface_area=1.85,
            description="Check",
            diabetes=False,
        )

        # Mock session returning None
        mock_exec = MagicMock()
        mock_exec.first.return_value = None
        mock_session.exec.return_value = mock_exec

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            create_medical_history(mock_session, patient_id, history_data, mock_user)

        assert exc.value.status_code == 404
        assert "Paciente no encontrado" in exc.value.detail
        mock_session.add.assert_not_called()

    @patch("app.services.medical_history.calcular_edad")
    def test_create_medical_history_db_error(
        self, mock_calc_edad, mock_session, mock_user, mock_patient
    ):
        # Arrange
        patient_id = "patient-123"
        history_data = MedicalHistoryCreate(
            smoking_status="never",
            sedentary_lifestyle=False,
            blood_pressure=120,
            ldl_cholesterol=100,
            fasting_blood_sugar=90,
            body_mass_index=22.0,
            recg="normal",
            height=175,
            weight=70,
            body_surface_area=1.85,
            description="Check",
            diabetes=False,
        )

        mock_exec = MagicMock()
        mock_exec.first.return_value = mock_patient
        mock_session.exec.return_value = mock_exec
        mock_calc_edad.return_value = 33

        # Simulate exception during commit
        mock_session.commit.side_effect = Exception("DB Connection Failed")

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            create_medical_history(mock_session, patient_id, history_data, mock_user)

        assert exc.value.status_code == 500
        assert "Error inesperado" in exc.value.detail
        mock_session.rollback.assert_called_once()

    def test_get_medical_histories_success(self, mock_session, mock_user, mock_patient):
        # Arrange
        patient_id = "patient-123"

        # Mock Finding Patient
        mock_exec_patient = MagicMock()
        mock_exec_patient.first.return_value = mock_patient

        # Mock Finding Histories
        mock_histories_list = [MagicMock(id="hist-1"), MagicMock(id="hist-2")]
        mock_exec_histories = MagicMock()
        mock_exec_histories.all.return_value = mock_histories_list

        # session.exec is called twice.
        # limit side_effect to return different mocks for successive calls
        mock_session.exec.side_effect = [mock_exec_patient, mock_exec_histories]

        # Act
        result = get_medical_histories_by_patient(mock_session, patient_id, mock_user)

        # Assert
        assert len(result) == 2
        assert result[0].id == "hist-1"

    def test_get_medical_histories_patient_not_found(self, mock_session, mock_user):
        # Arrange
        patient_id = "patient-unknown"

        mock_exec = MagicMock()
        mock_exec.first.return_value = None  # Patient not found
        mock_session.exec.return_value = mock_exec

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            get_medical_histories_by_patient(mock_session, patient_id, mock_user)

        assert exc.value.status_code == 404
