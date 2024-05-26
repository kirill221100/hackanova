from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, contains_eager
from schemes.user import UserCreateScheme
from db.models.user import User
from db.models.tag import Tag
from db.utils.tag import get_tags_by_names
from fastapi import HTTPException
from typing import List


async def get_user_by_id(user_id: int, session: AsyncSession):
    return (await session.execute(select(User).filter_by(id=user_id))).scalar_one_or_none()


async def get_user_by_id_with_tags(user_id: int, session: AsyncSession):
    return (await session.execute(select(User).filter_by(id=user_id).options(selectinload(User.tags)))).scalar_one_or_none()


async def get_all_users_with_tags(session: AsyncSession):
    return (await session.execute(
        select(User).options(selectinload(User.tags)))
            ).scalars().all()


async def get_users_by_tags(tags: List[str], session: AsyncSession):
    return (await session.execute(
        select(User).join(User.tags).filter(User.tags.any(Tag.name.in_(tags))).options(contains_eager(User.tags)))
            ).unique().scalars().all()


async def create_user(data: UserCreateScheme, session: AsyncSession):
    user = User()
    for k, v in data:
        if k != 'tags':
            setattr(user, k, v)
    tags = await get_tags_by_names(data.tags, session)
    user.tags = tags
    session.add(user)
    await session.commit()
    return user


async def update_tags_on_user(user_id: int, names: List[str], session: AsyncSession):
    user = await get_user_by_id_with_tags(user_id, session)
    # Get the list of tags from the database
    tags = await get_tags_by_names(names, session)
    # Assign the tags to the user
    user.tags = tags
    await session.commit()
    return {'message': 'updated'}
