"""
Organization Repository

All persistence access for organizations and org membership goes through
here. Kept together (rather than split into two repository files) since
every membership operation is meaningless without its organization,
mirroring how CollectionRepository owns both CollectionModel and
CollectionItemModel.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import OrganizationMemberModel, OrganizationModel


class OrganizationRepository:
    """Persistence access for Organization and OrganizationMember records."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> OrganizationModel:
        model = OrganizationModel(name=name)

        self.db.add(model)
        self.db.flush()

        return model

    def get(self, organization_id: str) -> OrganizationModel | None:
        return self.db.get(OrganizationModel, organization_id)

    def list_all(self) -> list[OrganizationModel]:
        return list(self.db.execute(select(OrganizationModel)).scalars())

    def add_member(
        self, organization_id: str, user_id: str, role: str = "member"
    ) -> OrganizationMemberModel:
        model = OrganizationMemberModel(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

        self.db.add(model)
        self.db.flush()

        return model

    def get_membership_for_user(
        self, user_id: str
    ) -> OrganizationMemberModel | None:
        """
        Returns the user's first/primary membership. Phase A only ever
        creates one membership per user (via signup), so "first" and
        "only" are the same thing today -- this becomes a real choice
        once org-switching exists.
        """

        stmt = select(OrganizationMemberModel).where(
            OrganizationMemberModel.user_id == user_id
        )

        return self.db.execute(stmt).scalars().first()
