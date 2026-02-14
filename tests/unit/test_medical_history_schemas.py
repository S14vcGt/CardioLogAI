import pytest
from pydantic import ValidationError
from app.schemas.medical_history import MedicalHistoryCreate, MedicalHistoryRead


class TestMedicalHistorySchema:

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
        assert model.date == "2023-10-10"
