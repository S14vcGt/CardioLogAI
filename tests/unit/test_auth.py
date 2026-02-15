from app.core.security import get_password_hash, verify_password


def test_password_hash_and_verify():
    password = "test1234"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
