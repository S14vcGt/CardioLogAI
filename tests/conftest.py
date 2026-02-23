'''import os
import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import get_session
from app.main import app
from fastapi.testclient import TestClient

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost/tesis_db_test")

test_engine = create_engine(TEST_DATABASE_URL, echo=True)

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture()
def session():
    with Session(test_engine) as session:
        yield session

@pytest.fixture()
def client(session):
    # Sobrescribir la dependencia de sesión en la app
    def get_test_session_override():
        yield session
    app.dependency_overrides[get_session] = get_test_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear() '''