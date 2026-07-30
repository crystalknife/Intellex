"""
Organization Repository

All persistence access for organizations and org membership goes through
here. Kept together (rather than split into two repository files) since
every membership operation is meaningless without its organization,
mirroring how CollectionRepository owns both CollectionModel and
CollectionItemModel.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from backend.app.db.models import (
    OrganizationInviteModel,
    OrganizationMemberModel,
    OrganizationModel,
)


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

    def list_members(
        self, organization_id: str
    ) -> list[OrganizationMemberModel]:
        stmt = (
            select(OrganizationMemberModel)
            .options(joinedload(OrganizationMemberModel.user))
            .where(OrganizationMemberModel.organization_id == organization_id)
            .order_by(OrganizationMemberModel.joined_at.asc())
        )

        return list(self.db.execute(stmt).scalars())

    def get_member(
        self, organization_id: str, user_id: str
    ) -> OrganizationMemberModel | None:
        stmt = select(OrganizationMemberModel).where(
            OrganizationMemberModel.organization_id == organization_id,
            OrganizationMemberModel.user_id == user_id,
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def count_owners(self, organization_id: str) -> int:
        return self.db.execute(
            select(func.count())
            .select_from(OrganizationMemberModel)
            .where(
                OrganizationMemberModel.organization_id == organization_id,
                OrganizationMemberModel.role == "owner",
            )
        ).scalar_one()

    def update_role(
        self, organization_id: str, user_id: str, role: str
    ) -> OrganizationMemberModel | None:
        member = self.get_member(organization_id, user_id)

        if member is None:
            return None

        member.role = role
        self.db.commit()
        self.db.refresh(member)

        return member

    def remove_member(self, organization_id: str, user_id: str) -> bool:
        member = self.get_member(organization_id, user_id)

        if member is None:
            return False

        self.db.delete(member)
        self.db.commit()

        return True

    # --- Invites -------------------------------------------------------

    def create_invite(
        self, organization_id: str, email: str, role: str, expires_at
    ) -> OrganizationInviteModel:
        invite = OrganizationInviteModel(
            organization_id=organization_id,
            email=email.lower(),
            role=role,
            expires_at=expires_at,
        )

        self.db.add(invite)
        self.db.commit()
        self.db.refresh(invite)

        return invite

    def get_invite_by_token(self, token: str) -> OrganizationInviteModel | None:
        return self.db.execute(
            select(OrganizationInviteModel).where(
                OrganizationInviteModel.token == token
            )
        ).scalar_one_or_none()

    def list_pending_invites(
        self, organization_id: str
    ) -> list[OrganizationInviteModel]:
        stmt = (
            select(OrganizationInviteModel)
            .where(
                OrganizationInviteModel.organization_id == organization_id,
                OrganizationInviteModel.accepted_at.is_(None),
            )
            .order_by(OrganizationInviteModel.created_at.desc())
        )

        return list(self.db.execute(stmt).scalars())

    def get_invite(
        self, organization_id: str, invite_id: str
    ) -> OrganizationInviteModel | None:
        return self.db.execute(
            select(OrganizationInviteModel).where(
                OrganizationInviteModel.id == invite_id,
                OrganizationInviteModel.organization_id == organization_id,
            )
        ).scalar_one_or_none()

    def revoke_invite(self, organization_id: str, invite_id: str) -> bool:
        invite = self.get_invite(organization_id, invite_id)

        if invite is None:
            return False

        self.db.delete(invite)
        self.db.commit()

        return True

    def mark_invite_accepted(self, invite: OrganizationInviteModel, when) -> None:
        invite.accepted_at = when
        self.db.commit()
