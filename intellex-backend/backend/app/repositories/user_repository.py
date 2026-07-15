"""
User Repository

All persistence access for users goes through here.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import UserModel


class UserRepository:
    """Persistence access for User records."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email.lower())

        return self.db.execute(stmt).scalar_one_or_none()

    def get(self, user_id: str) -> UserModel | None:
        return self.db.get(UserModel, user_id)

    def create(
        self, email: str, hashed_password: str, full_name: str = ""
    ) -> UserModel:
        model = UserModel(
            email=email.lower(),
            hashed_password=hashed_password,
            full_name=full_name,
        )

        self.db.add(model)
        self.db.flush()

        return model
