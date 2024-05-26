from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from db.db_setup import get_session
from db.utils.tag import create_tag, get_all_tags
from db.utils.team import get_teams_by_tags, update_tags_on_team
from db.utils.user import get_users_by_tags, update_tags_on_user
from schemes.tag import TagResponse, GetTeamByTagsSchemeResponse
from schemes.user import UserResponseScheme

tag_router = APIRouter()


@tag_router.post("/create", response_model=TagResponse)
async def create_tag_path(text: str, session: AsyncSession = Depends(get_session)):
    """только для тестов, не прод"""
    return await create_tag(text, session)


@tag_router.get("/get-teams-by-tags", response_model=List[GetTeamByTagsSchemeResponse])
async def get_teams_by_tags_path(tags: List[str] = Query(None), session: AsyncSession = Depends(get_session)):
    return await get_teams_by_tags(tags, session)


@tag_router.get("/get-users-by-tags", response_model=List[UserResponseScheme])
async def get_users_by_tags_path(tags: List[str] = Query(None), session: AsyncSession = Depends(get_session)):
    return await get_users_by_tags(tags, session)


@tag_router.get("/get-tag-list", response_model=List[TagResponse])
async def get_tag_list_path(session: AsyncSession = Depends(get_session)):
    return await get_all_tags(session)


@tag_router.post("/{user_id}/update-user-tags", response_model=dict)
async def update_user_tags_path(user_id: int, tags: List[str], session: AsyncSession = Depends(get_session)):
    """
    пример работы:
    например до изменений у юзера были тэги: python и backend.
    после отправки листа [python, java, ml] у юзера тэги будут такими: python, java, ml
    """
    return await update_tags_on_user(user_id=user_id, names=tags, session=session)


@tag_router.post("/{team_id}/update-team-tags", response_model=dict)
async def update_team_tags_path(team_id: int, tags: List[str], session: AsyncSession = Depends(get_session)):
    """
    пример работы:
    например до изменений у команды были тэги: python и backend.
    после отправки листа [python, java, ml] у юзера тэги будут такими: python, java, ml
    """
    return await update_tags_on_team(team_id=team_id, names=tags, session=session)
