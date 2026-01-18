import pytest

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "testpass", "full_name": "Test User", "email": "test@example.com"}

def test_register_and_login_user(client, user_data):
    # Registro
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200 or response.status_code == 400
    # Login
    response = client.post("/auth/token", data={"username": user_data["username"], "password": user_data["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data 

def test_create_user():
    
