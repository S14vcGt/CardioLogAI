import pytest
from app.models.patient import Patient
from app.models.user import User

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "testpass", "full_name": "Test User", "email": "test@example.com"}

@pytest.fixture
def patient_data():
    return {"name": "Test Patient", "birth_date": "1990-01-01"}

def test_create_and_get_patient(client, user_data, patient_data):
    # Register and login first to get token and current user
    client.post("/users/", json=user_data)
    response = client.post("/auth/token", data={"username": user_data["username"], "password": user_data["password"]})
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Create patient
    response = client.post("/patients/", json=patient_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == patient_data["name"]
    assert "id" in data
    patient_id = data["id"]

    # Get patients
    response = client.get("/patients/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["id"] == patient_id
