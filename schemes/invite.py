from pydantic import BaseModel
from schemes.tag import TagResponse
from typing import List, Optional
from db.models.invite import InviteStatus, InviteType


class InviteUserResponseScheme(BaseModel):
    first_name: str
    last_name: str
    avatar: Optional[str] = None


class AcceptInviteFromUserScheme(BaseModel):
    user_id: int


class RejectInviteFromUserScheme(BaseModel):
    user_id: int


class AcceptInviteScheme(BaseModel):
    user_id: int
    team_id: int


class RejectInviteScheme(BaseModel):
    user_id: int
    team_id: int


class InviteResponseScheme(BaseModel):
    user_id: int
    user: InviteUserResponseScheme
    team_id: int
    message: str
    type: InviteType
    status: InviteStatus


class CreateInviteScheme(BaseModel):
    user_id: int
    team_id: int
    message: str


class UserInviteResponseScheme(BaseModel):
    user_id: int
    team_id: int
    message: str
    status: InviteStatus
