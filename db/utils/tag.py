from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, literal
from sqlalchemy.orm import selectinload
from db.models.tag import Tag
from typing import List
from fastapi import HTTPException

from db.models.user import User


async def get_tags_by_names(names: List[str], session: AsyncSession):
    return (await session.execute(
        select(Tag).filter(Tag.name.in_(names)))
            ).scalars().all()


async def get_all_tags(session: AsyncSession):
    return (await session.execute(select(Tag))).scalars().all()


async def create_tag(name: str, session: AsyncSession):
    tag = Tag(name=name.lower())
    session.add(tag)
    await session.commit()
    return tag


async def update_tags_on_user(user_id: int, tags: List[str], session: AsyncSession):
    result = await session.execute(select(User).filter(User.id == literal(user_id)))
    user = result.scalar_one_or_none()
    # Get the list of tags from the database
    tags = List[str]
    # Assign the tags to the user
    user.tags.extend(tags)
    await session.commit()
    return user.tags
