from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, literal
from sqlalchemy.orm import selectinload
from db.models.tag import Tag
from typing import List
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


async def get_tags_by_names(names: List[str], session: AsyncSession):
    return (await session.execute(
        select(Tag).filter(Tag.name.in_(names)))
            ).scalars().all()


async def get_all_tags(session: AsyncSession):
    return (await session.execute(select(Tag))).scalars().all()


async def create_tag(name: str, session: AsyncSession):
    try:
        tag = Tag(name=name.lower())
        session.add(tag)
        await session.commit()
        return tag
    except IntegrityError as e:
        raise HTTPException(409, detail='Такой тег уже есть')
