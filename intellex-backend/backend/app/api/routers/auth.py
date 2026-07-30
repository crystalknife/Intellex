from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_membership, get_current_user
from backend.app.api.schemas.auth import (
    LoginRequest,
    MeResponse,
    OrganizationResponse,
    SignupRequest,
    TokenResponse,
    UserResponse,
)
from backend.app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from backend.app.db.models import OrganizationMemberModel, UserModel
from backend.app.db.session import get_db
from backend.app.repositories.organization_repository import (
    OrganizationRepository,
)
from backend.app.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def _issue_token(
    user: UserModel, org: OrganizationResponse, role: str
) -> TokenResponse:
    token = create_access_token(
        user_id=user.id, organization_id=org.id, role=role
    )

    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
        organization=org,
        role=role,
    )


@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)

    if user_repo.get_by_email(payload.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    org_repo = OrganizationRepository(db)
    invite = None

    if payload.invite_token:
        invite = org_repo.get_invite_by_token(payload.invite_token)

        if invite is None or invite.accepted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This invite link is invalid or has already been used",
            )

        if invite.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This invite link has expired",
            )

        if invite.email.lower() != payload.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This invite was issued to a different email address",
            )
    elif not payload.organization_name or not payload.organization_name.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="organization_name is required when signing up without an invite",
        )

    user = user_repo.create(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )

    if invite is not None:
        org = org_repo.get(invite.organization_id)
        role = invite.role
        org_repo.add_member(org.id, user.id, role=role)
        org_repo.mark_invite_accepted(invite, datetime.utcnow())
    else:
        org = org_repo.create(payload.organization_name.strip())
        role = "owner"
        # The first user in a newly created organization is always its owner.
        org_repo.add_member(org.id, user.id, role=role)

    db.commit()
    db.refresh(user)
    db.refresh(org)

    return _issue_token(user, OrganizationResponse.model_validate(org), role)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(payload.email)

    if user is None or not verify_password(
        payload.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    membership = OrganizationRepository(db).get_membership_for_user(user.id)

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to an organization",
        )

    org = OrganizationRepository(db).get(membership.organization_id)

    return _issue_token(
        user, OrganizationResponse.model_validate(org), membership.role
    )


@router.get("/me", response_model=MeResponse)
async def me(
    user: UserModel = Depends(get_current_user),
    membership: OrganizationMemberModel = Depends(get_current_membership),
    db: Session = Depends(get_db),
):
    org = OrganizationRepository(db).get(membership.organization_id)

    return MeResponse(
        user=UserResponse.model_validate(user),
        organization=OrganizationResponse.model_validate(org),
        role=membership.role,
    )
