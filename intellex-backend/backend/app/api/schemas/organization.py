from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


MemberRole = Literal["owner", "admin", "member"]


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    email: str
    full_name: str
    role: MemberRole
    joined_at: datetime

    @classmethod
    def from_model(cls, model) -> "MemberResponse":
        return cls(
            user_id=model.user_id,
            email=model.user.email,
            full_name=model.user.full_name,
            role=model.role,
            joined_at=model.joined_at,
        )


class MemberListResponse(BaseModel):
    items: list[MemberResponse]

    @classmethod
    def build(cls, models) -> "MemberListResponse":
        return cls(items=[MemberResponse.from_model(m) for m in models])


class UpdateMemberRoleRequest(BaseModel):
    role: MemberRole


class CreateInviteRequest(BaseModel):
    email: EmailStr
    role: MemberRole = "member"


class InviteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    role: MemberRole
    token: str
    created_at: datetime
    expires_at: datetime


class InviteListResponse(BaseModel):
    items: list[InviteResponse]
