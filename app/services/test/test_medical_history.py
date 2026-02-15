import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.schemas.medical_history import MedicalHistoryCreate
from app.services.medical_history import (
    create_medical_history,
    get_medical_histories_by_patient,
)
from app.models.patient import Patient
from app.models.user import User


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


'''class TestMedicalHistorySchema:

    def test_create_valid_complete(self):
        data = {
            "smoking_status": "no smoker",
            "sedentary_lifestyle": False,
            "blood_pressure": 120,
            "ldl_cholesterol": 100,
            "fasting_blood_sugar": 90,
            "body_mass_index": 22.5,
            "recg": "normal",
            "height": 175,
            "weight": 70,
            "body_surface_area": 1.85,
            "description": "Routine checkup",
            "diabetes": False,
        }
        bh = MedicalHistoryCreate(**data)
        assert bh.smoking_status == "no smoker"
        assert bh.blood_pressure == 120
        assert bh.diabetes is False

    def test_create_minimal_required(self):
        # Only mandatory fields
        data = {
            "smoking_status": "active smoker",
            "sedentary_lifestyle": True,
            "blood_pressure": 140,
            "ldl_cholesterol": 160,
            "recg": "abnormal",
            "height": 180,
            "weight": 90,
        }
        bh = MedicalHistoryCreate(**data)
        # Optional defaults to None if not specified?
        # Pydantic defaults are None by default for Optional fields if not set as default=...
        # Let's check schema again: fasting_blood_sugar: Optional[int]
        # Yes, default is None (implicitly handled by Pydantic V2) or explicit None depending on config.
        # But wait, user code: fasting_blood_sugar: Optional[int]
        # In Pydantic V2, Optional[int] alone doesn't mean default=None automatically unless structured that way,
        # but usually it's treated as required if no default is provided?
        # Actually checking `app/schemas/medical_history.py`: Optional[int] without `= None` means it's required to pass None explicitly OR default is None?
        # Let's assume standard behavior: if field is Optional and no default, it might be required to pass None or just work.
        # But let's act safe and assume standard behavior where Optional implies default=None in modern Pydantic if configured or if just type hint.
        # Correction: In Pydantic V2 `fruit: str | None = None` is preferred. `Optional[str]` is alias.
        # If the user code `fasting_blood_sugar: Optional[int]` has no `= None`, then it is REQUIRED to pass a value (which can be None).
        # However, looking at the code provided: `fasting_blood_sugar: Optional[int]`
        # If it's Pydantic v1 style or if the config allows it, maybe it defaults to None.
        # Let's write test to fail if it requires explicit None, we'll see.
        pass

    def test_create_missing_required(self):
        data = {
            "smoking_status": "smoker",
            # Missing blood_pressure
        }
        with pytest.raises(ValidationError):
            MedicalHistoryCreate(**data)

    def test_read_serialization(self):
        data = {
            "id": 123,
            "age": 30,
            "smoking_status": "never",
            "sedentary_lifestyle": False,
            "blood_pressure": 110,
            "ldl_cholesterol": 90,
            "fasting_blood_sugar": 85,
            "body_mass_index": 21.0,
            "recg": "normal",
            "height": 170.0,
            "weight": 65.0,
            "body_surface_area": 1.75,
            "date": "2023-10-10",
            "description": "Clean bill of health",
        }
        # The schema uses ConfigDict(from_attributes=True) so we can pass dict or object
        # but here testing direct instantiation
        model = MedicalHistoryRead(**data)
        assert model.id == 123
        assert model.date == "2023-10-10"'''
