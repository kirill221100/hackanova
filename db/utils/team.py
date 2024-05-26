from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, contains_eager
from db.models.team import Team, TeamStatus
from db.models.tag import Tag
from db.utils.tag import get_tags_by_names
from fastapi import HTTPException
from schemes.team import TeamSearchScheme, TeamCreateScheme
from typing import List


async def get_team_by_id(team_id: int, session: AsyncSession):
    if res := (await session.execute(
        select(Team).filter_by(id=team_id))
            ).scalar_one_or_none():
        return res
    raise HTTPException(404, 'Нет команды с таким id')


async def get_team_by_id_with_users_and_tags(team_id: int, session: AsyncSession):
    if res := (await session.execute(
        select(Team).filter_by(id=team_id).options(selectinload(Team.participants), selectinload(Team.tags)))
            ).scalar_one_or_none():
        return res
    raise HTTPException(404, 'Нет команды с таким id')


async def get_team_by_id_with_users(team_id: int, session: AsyncSession):
    if res := (await session.execute(
        select(Team).filter_by(id=team_id).options(selectinload(Team.participants)))
            ).scalar_one_or_none():
        return res
    raise HTTPException(404, 'Нет команды с таким id')


async def get_all_teams_with_users_and_tags(session: AsyncSession):
    return (await session.execute(
        select(Team).options(selectinload(Team.participants), selectinload(Team.tags)))
            ).scalars().all()


async def get_team_by_id_with_tags(team_id: int, session: AsyncSession):
    if res := (await session.execute(
        select(Team).filter_by(id=team_id).options(selectinload(Team.tags)))
            ).scalar_one_or_none():
        return res
    raise HTTPException(404, 'Нет команды с таким id')


async def get_team_desc_and_tags(team_id: int, session: AsyncSession):
    if res := (await session.execute(
        select(Team).filter_by(id=team_id).options(selectinload(Team.tags)))
            ).scalar_one_or_none():
        return res
    raise HTTPException(404, 'Нет команды с таким id')


async def set_team_desc_and_tags(team_id: int, data: TeamSearchScheme, session: AsyncSession):
    team = await get_team_by_id_with_tags(team_id, session)
    team.team_description = data.team_description
    team.search_user_description = data.search_user_description
    tags = await get_tags_by_names(data.tags, session)
    team.tags = tags
    await session.commit()
    return {"message": "create"}


async def get_teams_by_tags(tags: List[str], session: AsyncSession):
    return (await session.execute(
        select(Team).join(Team.tags).filter(Team.tags.any(Tag.name.in_(tags))).options(contains_eager(Team.tags)))
            ).unique().scalars().all()


async def create_team(data: TeamCreateScheme, session: AsyncSession):
    team = Team()
    for k, v in data:
        if k != 'tags' and v is not None:
            setattr(team, k, v)

    team.tags = await get_tags_by_names(data.tags, session)
    session.add(team)
    await session.commit()
    return team


async def update_tags_on_team(team_id: int, names: List[str], session: AsyncSession):
    team = await get_team_by_id_with_tags(team_id, session)
    tags = await get_tags_by_names(names, session)
    team.tags = tags
    await session.commit()
    return {'message': 'updated'}


async def change_team_status(team_id: int, status: TeamStatus, session: AsyncSession):
    team = await get_team_by_id(team_id, session)
    if team.status != status:
        team.status = status
        await session.commit()
    return {'message': 'Done'}
