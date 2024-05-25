from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from db.db_setup import get_session
from db.utils.user import create_user, get_user_by_id_with_tags
from db.utils.invite import get_invitations, InviteType, accept_invite, reject_invite, create_invite
from schemes.invite import UserInviteResponseScheme, AcceptInviteScheme, RejectInviteScheme, CreateInviteScheme
from schemes.user import UserCreateScheme, UserResponseScheme
from db.models.invite import InviteType


user_router = APIRouter()


# class UserCreate(BaseModel):
#     name: str
#     second_name: Optional[str]
#     email: str
#     phone: Optional[str]
#     experience: Optional[str]
#     education: Optional[str]
#     about_me: Optional[str]
#     status_team: bool
#     hashtags: Optional[List[str]]
#
#
# class UserRead(BaseModel):
#     id: int
#     name: str
#     second_name: Optional[str]
#     email: str
#     phone: Optional[str]
#     experience: Optional[str]
#     education: Optional[str]
#     about_me: Optional[str]
#     status_team: bool
#     hashtags: Optional[List[str]]


@user_router.post("/create", response_model=UserResponseScheme)
async def create_user_path(data: UserCreateScheme, session: AsyncSession = Depends(get_session)):
    """только для тестов, не прод"""
    return await create_user(data, session)


@user_router.get("/{user_id}/get-user", response_model=UserResponseScheme)
async def get_user_path(user_id: int, session: AsyncSession = Depends(get_session)):
    return await get_user_by_id_with_tags(user_id, session)



@user_router.get("/{user_id}/get-invitations-from-user", response_model=List[UserInviteResponseScheme])
async def all_invitations_from_user_path(user_id: int, session: AsyncSession = Depends(get_session)):
    """приглашения отправленные юзером"""
    return await get_invitations(InviteType.TO_TEAM, session, user_id=user_id)


@user_router.get("/{user_id}/get-invitations-from-team", response_model=List[UserInviteResponseScheme])
async def all_invitations_from_team_path(user_id: int, session: AsyncSession = Depends(get_session)):
    """приглашения отправленные из команды юзеру"""
    return await get_invitations(InviteType.TO_USER, session, user_id=user_id)


@user_router.patch('/accept-invite', response_model=dict)
async def accept_invite_path(data: AcceptInviteScheme, session: AsyncSession = Depends(get_session)):
    """принять приглашение от команды"""
    return await accept_invite(InviteType.TO_USER, data, session)


@user_router.patch('/reject-invite', response_model=dict)
async def reject_invite_path(data: RejectInviteScheme, session: AsyncSession = Depends(get_session)):
    """отклонить приглашение от команды"""
    return await reject_invite(InviteType.TO_USER, data, session)


@user_router.post("/send-invite", response_model=dict)
async def send_invite_path(data: CreateInviteScheme, session: AsyncSession = Depends(get_session)):
    """отправить приглашение в команду"""
    return await create_invite(InviteType.TO_TEAM, data, session)


# @user_router.get("/", response_model=List[UserRead])
# async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
#     result = await db.execute(select(User).offset(skip).limit(limit))
#     users = result.scalars().all()
#     return users
#
#
# @user_router.get("/{user_id}", response_model=UserRead)
# async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
#     result = await db.execute(select(User).filter(User.id == literal(user_id)))
#     user = result.scalar_one_or_none()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
#
# @user_router.put("/{user_id}", response_model=UserRead)
# async def update_user(user_id: int, updated_user: UserCreate, db: AsyncSession = Depends(get_session)):
#     result = await db.execute(select(User).filter(User.id == literal(user_id)))
#     user = result.scalar_one_or_none()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     for key, value in updated_user.dict().items():
#         setattr(user, key, value)
#     await db.commit()
#     await db.refresh(user)
#     return user
#
#
# @user_router.delete("/{user_id}", response_model=UserRead)
# async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
#     result = await db.execute(select(User).filter(User.id == literal(user_id)))
#     user = result.scalar_one_or_none()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     await db.delete(user)
#     await db.commit()
#     return user
