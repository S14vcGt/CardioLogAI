import pytest
from unittest.mock import MagicMock, patch
from app.services import user as user_service
from app.schemas.user import UserCreate
from app.models.user import User

@pytest.fixture
def mock_session():
    return MagicMock()

def test_create_user(mock_session):
    user_create = UserCreate(
        username="testuser",
        password="password123",
        email="test@example.com",
        full_name="Test User"
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
        full_name="Admin User"
    )
    
    with patch("app.services.user.get_password_hash") as mock_hash:
        mock_hash.return_value = "hashed_secret"
        
        result = user_service.create(mock_session, user_create, is_admin=True)
        
        assert result.is_admin is True

def test_read_by_id(mock_session):
    user_id = "user-123"
    mock_user = User(id=user_id, username="testuser", email="test@example.com", hashed_password="pwd")
    
    # Mock exec().first()
    mock_exec = mock_session.exec.return_value
    mock_exec.first.return_value = mock_user
    
    result = user_service.read_by_id(mock_session, user_id)
    
    assert result == mock_user
    mock_session.exec.assert_called_once()

def test_read_all(mock_session):
    mock_users = [
        User(id="1", username="user1", email="u1@e.com", hashed_password="pwd"),
        User(id="2", username="user2", email="u2@e.com", hashed_password="pwd")
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
    mock_user = User(id="123", username=username, email="test@example.com", hashed_password="pwd")
    
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
    
    result = user_service.get_by_username(mock_session, username)
    
    assert result is None
