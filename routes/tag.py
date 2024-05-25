from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from db.db_setup import get_session
from db.utils.tag import create_tag, get_all_tags
from db.utils.team import get_team_by_tags
from schemes.tag import TagResponse, GetTeamByTagsSchemeResponse


tag_router = APIRouter()


@tag_router.post("/create", response_model=TagResponse)
async def create_tag_path(text: str, session: AsyncSession = Depends(get_session)):
    return await create_tag(text, session)


@tag_router.get("/get-team-by-tags", response_model=List[GetTeamByTagsSchemeResponse])
async def get_team_by_tags_path(tags: List[str] = Query(None), session: AsyncSession = Depends(get_session)):
    return await get_team_by_tags(tags, session)


@tag_router.get("/get-tag-list", response_model=List[TagResponse])
async def get_tag_list_path(session: AsyncSession = Depends(get_session)):
    return await get_all_tags(session)
