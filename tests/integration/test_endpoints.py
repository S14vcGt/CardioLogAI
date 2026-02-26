"""
Tests de integración para los endpoints de la API.

Flujo: registro → login → crear paciente → listar pacientes → crear historia → listar historias.
Menos es más: cada test verifica un endpoint clave con datos reales contra SQLite.
"""

import pytest


# ============================================================
# Auth
# ============================================================


class TestAuth:

    def test_register_and_login(self, client):
        """Registro + login exitoso devuelve access_token."""
        # Registro
        res = client.post("/users/", json={
            "username": "newuser",
            "password": "pass1234",
            "email": "new@test.com",
            "full_name": "New User",
        })
        assert res.status_code == 200
        assert res.json()["username"] == "newuser"

        # Login
        res = client.post("/auth/token", data={
            "username": "newuser",
            "password": "pass1234",
        })
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Login con contraseña incorrecta devuelve 400."""
        client.post("/users/", json={
            "username": "wrongpass",
            "password": "correct",
            "email": "wp@test.com",
            "full_name": "Wrong Pass",
        })
        res = client.post("/auth/token", data={
            "username": "wrongpass",
            "password": "incorrect",
        })
        assert res.status_code == 400

    def test_protected_endpoint_no_token(self, client):
        """Acceso sin token a endpoint protegido devuelve 401."""
        res = client.get("/patients/")
        assert res.status_code == 401


# ============================================================
# Users
# ============================================================


class TestUsers:

    def test_get_me(self, client, auth_headers):
        """GET /users/me devuelve el usuario autenticado."""
        res = client.get("/users/me", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["username"] == "testdoctor"
        assert data["email"] == "doctor@test.com"

    def test_duplicate_user(self, client):
        """Crear usuario duplicado devuelve 400."""
        user = {
            "username": "duplicate",
            "password": "pass1234",
            "email": "dup@test.com",
            "full_name": "Dup User",
        }
        client.post("/users/", json=user)
        res = client.post("/users/", json=user)
        assert res.status_code == 400


# ============================================================
# Patients
# ============================================================


class TestPatients:

    def test_create_and_list_patients(self, client, auth_headers):
        """Crear paciente y recuperarlo en la lista."""
        patient = {
            "name": "Carlos",
            "lastname": "Pérez",
            "birth_date": "1990-05-15",
            "address": "Av. Bolivar 123",
            "cedula": 20123456,
            "phone": "0414-1234567",
            "email": "carlos@test.com",
            "sex": "M",
            "family_history": True,
            "doctor_id": None,
        }

        # Crear
        res = client.post("/patients/", json=patient, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["name"] == "Carlos"
        assert "id" in data
        patient_id = data["id"]

        # Listar
        res = client.get("/patients/", headers=auth_headers)
        assert res.status_code == 200
        patients = res.json()
        assert len(patients) >= 1
        assert any(p["id"] == patient_id for p in patients)


# ============================================================
# Medical Histories
# ============================================================


class TestMedicalHistories:

    @pytest.fixture()
    def patient_id(self, client, auth_headers):
        """Crea un paciente y devuelve su ID para usarlo en tests de historias."""
        res = client.post("/patients/", json={
            "name": "Ana",
            "lastname": "García",
            "birth_date": "1985-03-20",
            "address": "Calle 10",
            "cedula": 30987654,
            "phone": "0412-9876543",
            "email": "ana@test.com",
            "sex": "F",
            "family_history": False,
            "doctor_id": None,
        }, headers=auth_headers)
        return res.json()["id"]

    def test_create_and_list_histories(self, client, auth_headers, patient_id):
        """Crear historia médica y recuperarla en la lista."""
        history = {
            "smoking_status": "never",
            "sedentary_lifestyle": False,
            "blood_pressure": 120,
            "ldl_cholesterol": 100,
            "fasting_blood_sugar": 90,
            "body_mass_index": 22.0,
            "recg": "normal",
            "height": 170,
            "weight": 65,
            "body_surface_area": 1.75,
            "description": "Control de rutina",
            "diabetes": False,
            "heart_disease": False,
        }

        # Crear
        res = client.post(
            f"/patients/{patient_id}/histories/",
            json=history,
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["smoking_status"] == "never"
        assert data["blood_pressure"] == 120
        assert "age" in data  # calculado automáticamente
        assert "id" in data

        # Listar
        res = client.get(
            f"/patients/{patient_id}/histories/",
            headers=auth_headers,
        )
        assert res.status_code == 200
        histories = res.json()
        assert len(histories) == 1
        assert histories[0]["description"] == "Control de rutina"

    def test_create_history_patient_not_found(self, client, auth_headers):
        """Crear historia para paciente inexistente devuelve 404."""
        history = {
            "smoking_status": "never",
            "sedentary_lifestyle": False,
            "blood_pressure": 120,
            "ldl_cholesterol": 100,
            "fasting_blood_sugar": 90,
            "body_mass_index": 22.0,
            "recg": "normal",
            "height": 170,
            "weight": 65,
            "body_surface_area": 1.75,
            "description": "Test",
            "diabetes": False,
            "heart_disease": False,
        }
        res = client.post(
            "/patients/fake-id-123/histories/",
            json=history,
            headers=auth_headers,
        )
        assert res.status_code == 404
