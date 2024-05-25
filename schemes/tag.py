from pydantic import BaseModel


class TagResponse(BaseModel):
    id: int
    name: str


class GetTeamByTagsSchemeResponse(BaseModel):
    id: int
    name: str
