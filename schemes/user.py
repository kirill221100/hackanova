from pydantic import BaseModel, model_validator, EmailStr, model_validator
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


class UserUpdateScheme(UserCreateScheme):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    hackathon_search: Optional[bool] = None
    job_search: Optional[bool] = None
    status_team: Optional[UserTeamStatus] = None
    tags: Optional[Annotated[List[str], Len(min_length=1)]] = None

    @model_validator(mode='after')
    @classmethod
    def validate_given_values(cls, field_values):
        dict_values = dict(field_values)
        vals = list(map(lambda x: dict_values[x] is not None, dict_values))
        print(vals)
        assert vals.count(True) >= 1, "Нет данных на которые нужно изменить"
        return field_values
