"""
Security

Password hashing (bcrypt, called directly rather than through passlib --
passlib's bcrypt backend has had version-compatibility breakage, and the
bcrypt package's own API is small enough that the extra dependency layer
isn't earning its keep) and JWT issuing/verification for auth.
"""

from datetime import datetime, timedelta, UTC

import bcrypt
import jwt

from backend.app.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    *, user_id: str, organization_id: str, role: str
) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "org_id": organization_id,
        "role": role,
        "exp": expires_at,
    }

    return jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )


class InvalidTokenError(Exception):
    """Raised when a bearer token is missing, malformed, or expired."""


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError as e:
        raise InvalidTokenError(str(e)) from e
