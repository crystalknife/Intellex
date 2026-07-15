"""
Auth Dependencies

FastAPI dependencies for protected routes. Nothing in the rest of the
API uses these yet (Phase A is additive-only, per the auth rollout
plan) -- routers adopt `get_current_user`/`get_current_membership` as
part of the Phase B tenancy retrofit, one router at a time.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.app.core.security import InvalidTokenError, decode_access_token
from backend.app.db.models import OrganizationMemberModel, UserModel
from backend.app.db.session import get_db
from backend.app.repositories.organization_repository import (
    OrganizationRepository,
)
from backend.app.repositories.user_repository import UserRepository

_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        _bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> UserModel:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(credentials.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserRepository(db).get(payload["sub"])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_membership(
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OrganizationMemberModel:
    membership = OrganizationRepository(db).get_membership_for_user(user.id)

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to an organization",
        )

    return membership
