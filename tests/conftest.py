"""
Configuración compartida para tests de integración.

Usa SQLite en memoria para evitar dependencias externas.
Sobreescribe la sesión de la app con la sesión de prueba.
"""

import os
import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.core.config import get_session
from app.main import app
from pathlib import Path
from dotenv import load_dotenv

os.environ["TESTING"] = "1"

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crea las tablas al inicio y las elimina al final."""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture()
def session():
    """Sesión limpia por test con rollback automático."""
    with Session(test_engine) as session:
        yield session
        # Limpiar datos después de cada test
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.exec(table.delete())
        session.commit()


@pytest.fixture()
def client(session):
    """TestClient con la sesión de prueba inyectada."""

    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client):
    """Registra un usuario y devuelve headers con token JWT."""
    user_data = {
        "username": "testdoctor",
        "password": "securepass123",
        "email": "doctor@test.com",
        "full_name": "Test Doctor",
    }
    client.post("/users/", json=user_data)

    response = client.post(
        "/auth/token",
        data={"username": "testdoctor", "password": "securepass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}