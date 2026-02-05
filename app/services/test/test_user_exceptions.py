import pytest
from unittest.mock import MagicMock, patch
from app.services import user as user_service
from app.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

@pytest.fixture
def mock_session():
    return MagicMock()

def test_create_user_integrity_error(mock_session):
    user_create = UserCreate(
        username="duplicate_user",
        password="password123",
        email="duplicate@example.com",
        full_name="Duplicate User"
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
        full_name="Error User"
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
