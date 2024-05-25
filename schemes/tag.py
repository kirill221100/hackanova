from pydantic import BaseModel
from db.models.tag import T


class TagResponse(BaseModel):
    id: int
    text: str
