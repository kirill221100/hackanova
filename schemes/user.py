from pydantic import BaseModel, model_validator, EmailStr
from typing import Optional, List, Annotated
from db.models.user import UserTeamStatus
from schemes.tag import TagResponse
from annotated_types import Len


class UserCreateScheme(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    about_me: Optional[str] = None
    hackathon_search: bool
    job_search: bool
    status_team: UserTeamStatus
    avatar: Optional[str] = None
    vk: Optional[str] = None
    github: Optional[str] = None
    telegram: Optional[str] = None
    tags: Annotated[List[str], Len(min_length=1)]


class UserResponseScheme(UserCreateScheme):
    id: int
    tags: List[TagResponse]
