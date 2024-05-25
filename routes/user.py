from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from db.db_setup import get_session
from db.models.user import User
from sqlalchemy.sql.expression import literal
from pydantic import BaseModel

user_router = APIRouter()


class UserCreate(BaseModel):
    name: str
    second_name: Optional[str]
    email: str
    phone: Optional[str]
    experience: Optional[str]
    education: Optional[str]
    about_me: Optional[str]
    status_team: bool
    hashtags: Optional[List[str]]


class UserRead(BaseModel):
    id: int
    name: str
    second_name: Optional[str]
    email: str
    phone: Optional[str]
    experience: Optional[str]
    education: Optional[str]
    about_me: Optional[str]
    status_team: bool
    hashtags: Optional[List[str]]


@user_router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = User(
        name=user.name,
        second_name=user.second_name,
        email=user.email,
        phone=user.phone,
        experience=user.experience,
        education=user.education,
        about_me=user.about_me,
        status_team=user.status_team,
        hashtags=user.hashtags
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@user_router.get("/", response_model=List[UserRead])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


@user_router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).filter(User.id == literal(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, updated_user: UserCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).filter(User.id == literal(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_user.dict().items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


@user_router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).filter(User.id == literal(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return user
