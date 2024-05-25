from pydantic import BaseModel
from schemes.tag import TagResponse
from typing import List, Optional
from db.models.invite import InviteStatus


class InviteUserResponseScheme(BaseModel):
    first_name: str
    last_name: str
    avatar: Optional[str] = None


class AcceptInviteScheme(BaseModel):
    user_id: int


class RejectInviteScheme(BaseModel):
    user_id: int


class InviteResponseScheme(BaseModel):
    user_id: int
    user: InviteUserResponseScheme
    team_id: int
    message: str
    status: InviteStatus


class InviteScheme(BaseModel):
    user_id: int
    message: str


class UserInviteResponseScheme(BaseModel):
    user_id: int
    team_id: int
    message: str
    status: InviteStatus
