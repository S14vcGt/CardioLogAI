
from dotenv import load_dotenv
from app.services.auth import get_password_hash, verify_password

load_dotenv(dotenv_path=".env")

def test_password_hash_and_verify():
    password = "test1234"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) 