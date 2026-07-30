"""
Organization Router

Team/member management, plus invite creation to bring new people in.

There's no email infrastructure in this project, so invites don't send
mail -- POST /organization/invites returns a token that the owner shares
with the invitee out-of-band (copy a link, paste it in Slack, whatever).
The invitee redeems it via the optional invite_token field on
POST /auth/signup, which joins them directly to the inviting org instead
of creating a new one for them, preserving the existing
single-org-per-user model rather than introducing multi-org membership
and everything that would require (an org switcher, a "which org is
this token for" concept, etc.) -- see auth.py for the signup-side half
of this.

Authorization: any member can view the member/invite lists. Only
owners can invite, remove, or change roles -- kept intentionally simple
(no admin-vs-owner distinction in what they're allowed to manage)
rather than building a fuller permission matrix nothing has asked for.
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_membership
from backend.app.api.schemas import (
    CreateInviteRequest,
    InviteListResponse,
    InviteResponse,
    MemberListResponse,
    MemberResponse,
    UpdateMemberRoleRequest,
)
from backend.app.db.models import OrganizationMemberModel
from backend.app.db.session import get_db
from backend.app.repositories.organization_repository import (
    OrganizationRepository,
)
from backend.app.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/organization",
    tags=["Organization"],
)

_INVITE_EXPIRY_DAYS = 7


def _require_owner(membership: OrganizationMemberModel) -> None:
    if membership.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only an organization owner can do this",
        )


@router.get("/members", response_model=MemberListResponse)
async def list_members(
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    members = OrganizationRepository(db).list_members(membership.organization_id)

    return MemberListResponse.build(members)


@router.patch("/members/{user_id}", response_model=MemberResponse)
async def update_member_role(
    user_id: str,
    payload: UpdateMemberRoleRequest,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    _require_owner(membership)

    org_repo = OrganizationRepository(db)
    org_id = membership.organization_id

    target = org_repo.get_member(org_id, user_id)

    if target is None:
        raise HTTPException(status_code=404, detail="Member not found")

    if (
        target.role == "owner"
        and payload.role != "owner"
        and org_repo.count_owners(org_id) <= 1
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Can't change this member's role -- they're the "
                "organization's only owner. Promote someone else to "
                "owner first."
            ),
        )

    updated = org_repo.update_role(org_id, user_id, payload.role)

    return MemberResponse.from_model(updated)


@router.delete("/members/{user_id}", status_code=204)
async def remove_member(
    user_id: str,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    _require_owner(membership)

    org_repo = OrganizationRepository(db)
    org_id = membership.organization_id

    target = org_repo.get_member(org_id, user_id)

    if target is None:
        raise HTTPException(status_code=404, detail="Member not found")

    if target.role == "owner" and org_repo.count_owners(org_id) <= 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Can't remove this member -- they're the organization's "
                "only owner. Promote someone else to owner first."
            ),
        )

    org_repo.remove_member(org_id, user_id)


@router.get("/invites", response_model=InviteListResponse)
async def list_invites(
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    _require_owner(membership)

    invites = OrganizationRepository(db).list_pending_invites(
        membership.organization_id
    )

    return InviteListResponse(items=invites)


@router.post("/invites", response_model=InviteResponse, status_code=201)
async def create_invite(
    payload: CreateInviteRequest,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    _require_owner(membership)

    org_repo = OrganizationRepository(db)
    org_id = membership.organization_id

    existing_user = UserRepository(db).get_by_email(payload.email)
    if existing_user is not None and org_repo.get_membership_for_user(
        existing_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "This person already has an Intellex account and "
                "organization. Multi-organization membership isn't "
                "supported yet."
            ),
        )

    expires_at = datetime.utcnow() + timedelta(days=_INVITE_EXPIRY_DAYS)

    invite = org_repo.create_invite(
        org_id, payload.email, payload.role, expires_at
    )

    return InviteResponse.model_validate(invite)


@router.delete("/invites/{invite_id}", status_code=204)
async def revoke_invite(
    invite_id: str,
    db: Session = Depends(get_db),
    membership: OrganizationMemberModel = Depends(get_current_membership),
):
    _require_owner(membership)

    if not OrganizationRepository(db).revoke_invite(
        membership.organization_id, invite_id
    ):
        raise HTTPException(status_code=404, detail="Invite not found")
