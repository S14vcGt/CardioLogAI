import pytest
from unittest.mock import MagicMock, patch
from app.services import user as user_service
from app.schemas.user import UserCreate
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


@pytest.fixture
def mock_session():
    return MagicMock()


def test_create_user(mock_session):
    user_create = UserCreate(
        username="testuser",
        password="password123",
        email="test@example.com",
        full_name="Test User",
    )

    # Mocking get_password_hash to return a fixed string
    with patch("app.services.user.get_password_hash") as mock_hash:
        mock_hash.return_value = "hashed_secret"

        result = user_service.create(mock_session, user_create)

        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.hashed_password == "hashed_secret"
        assert result.is_admin is False

        # Verify session interactions
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()


def test_create_admin_user(mock_session):
    user_create = UserCreate(
        username="adminuser",
        password="password123",
        email="admin@example.com",
        full_name="Admin User",
    )

    with patch("app.services.user.get_password_hash") as mock_hash:
        mock_hash.return_value = "hashed_secret"

        result = user_service.create(mock_session, user_create, is_admin=True)

        assert result.is_admin is True


def test_create_user_integrity_error(mock_session):
    user_create = UserCreate(
        username="duplicate_user",
        password="password123",
        email="duplicate@example.com",
        full_name="Duplicate User",
    )

    # Mock commit to raise IntegrityError
    # IntegrityError constructor arguments: statement, params, orig
    mock_session.commit.side_effect = IntegrityError("statement", "params", "orig")

    with patch("app.services.user.get_password_hash") as mock_hash:
        mock_hash.return_value = "hashed_secret"

        with pytest.raises(HTTPException) as exc_info:
            user_service.create(mock_session, user_create)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Usuario o Email ya registrado"
        mock_session.rollback.assert_called_once()


def test_create_user_general_exception(mock_session):
    user_create = UserCreate(
        username="error_user",
        password="password123",
        email="error@example.com",
        full_name="Error User",
    )

    # Mock commit to raise a general Exception
    mock_session.commit.side_effect = Exception("Database connection failed")

    with patch("app.services.user.get_password_hash") as mock_hash:
        mock_hash.return_value = "hashed_secret"

        with pytest.raises(HTTPException) as exc_info:
            user_service.create(mock_session, user_create)

        assert exc_info.value.status_code == 500
        assert "Error inesperado" in exc_info.value.detail
        mock_session.rollback.assert_called_once()


def test_read_by_id(mock_session):
    user_id = "user-123"
    mock_user = User(
        id=user_id, username="testuser", email="test@example.com", hashed_password="pwd"
    )

    # Mock exec().first()
    mock_exec = mock_session.exec.return_value
    mock_exec.first.return_value = mock_user

    result = user_service.read_by_id(mock_session, user_id)

    assert result == mock_user
    mock_session.exec.assert_called_once()


def test_read_all(mock_session):
    mock_users = [
        User(id="1", username="user1", email="u1@e.com", hashed_password="pwd"),
        User(id="2", username="user2", email="u2@e.com", hashed_password="pwd"),
    ]

    # Mock exec().all()
    mock_exec = mock_session.exec.return_value
    mock_exec.all.return_value = mock_users

    result = user_service.read_all(mock_session)

    assert len(result) == 2
    assert result == mock_users
    mock_session.exec.assert_called_once()


def test_get_by_username(mock_session):
    username = "testuser"
    mock_user = User(
        id="123", username=username, email="test@example.com", hashed_password="pwd"
    )

    # Mock exec().first()
    mock_exec = mock_session.exec.return_value
    mock_exec.first.return_value = mock_user

    result = user_service.get_by_username(mock_session, username)

    assert result == mock_user
    mock_session.exec.assert_called_once()


def test_get_by_username_not_found(mock_session):
    username = "unknown"

    # Mock exec().first() returning None
    mock_exec = mock_session.exec.return_value
    mock_exec.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.get_by_username(mock_session, username)

    assert exc_info.value.status_code == 404
    assert "Usuario no encontrado" in exc_info.value.detail


def test_get_by_username_unexpected_error(mock_session):
    mock_session.exec.side_effect = Exception("Conexión perdida con la DB")

    with pytest.raises(HTTPException) as exc_info:
        user_service.get_by_username(mock_session, "usuario_prueba")

    assert exc_info.value.status_code == 500

    assert "Error inesperado" in exc_info.value.detail
    assert "Conexión perdida con la DB" in exc_info.value.detail
