from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.models.team import Team
from db.utils.tag import get_tags_by_names
from fastapi import HTTPException
from schemes.team import TeamSearch
from typing import List


async def get_team_by_id(team_id: int, session: AsyncSession):
    return (await session.execute(
        select(Team).filter_by(id=team_id).options(selectinload(Team.participants)))
            ).scalar_one_or_none()


async def get_team_desc_and_tags(team_id: int, session: AsyncSession):
    return (await session.execute(
        select(Team).filter_by(id=team_id).options(selectinload(Team.tags)))
            ).scalar_one_or_none()


async def set_team_desc_and_tags(team_id: int, data: TeamSearch, session: AsyncSession):
    team = await get_team_by_id(team_id, session)
    team.description = data.description
    tags = await get_tags_by_names(data.tags, session)
    team.tags.extend(tags)
    await session.commit()
    return {"message": "create"}


async def get_team_by_tags(tags: List[str], session: AsyncSession):
    return (await session.execute(
        select(Team).filter(Team.tags.name.in_(tags)))
            ).scalars().all()

