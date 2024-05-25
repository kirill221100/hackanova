from pydantic import BaseModel, ConfigDict
from annotated_types import Len
from schemes.tag import TagResponse
from typing import List, Annotated, Optional
from db.models.team import TeamStatus


class TeamSearchScheme(BaseModel):
    description: str
    tags: List[str]


class TeamSearchResponseScheme(BaseModel):
    description: str
    tags: List[TagResponse]


class TeamSearchUserScheme(BaseModel):
    id: int
    first_name: str
    last_name: str


class TeamResponseScheme(BaseModel):
    id: int
    name: str
    description: str
    task: str
    participants: List[TeamSearchUserScheme]


class TeamCreateScheme(BaseModel):
    name: str
    description: str
    task: str
    tags: Annotated[List[str], Len(min_length=1)]
    status: TeamStatus


class TeamCreateResponseScheme(TeamCreateScheme):
    tags: List[TagResponse]


class TeamByTags(BaseModel):
    tags: List[str]
