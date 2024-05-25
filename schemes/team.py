from pydantic import BaseModel
from schemes.tag import TagResponse


class TeamSearch(BaseModel):
    description: str
    tags: List[TagResponse]
