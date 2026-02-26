import hashlib
import base64
import bcrypt


def _pre_hash(password: str) -> bytes:
    """Pre-hash password with SHA-256 to avoid bcrypt's 72-byte limit."""
    return base64.b64encode(hashlib.sha256(password.encode("utf-8")).digest())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        _pre_hash(plain_password),
        hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        _pre_hash(password),
        bcrypt.gensalt(),
    ).decode("utf-8")
