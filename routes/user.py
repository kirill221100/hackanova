from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from db.db_setup import get_session
from db.models.user import User
from db.models.team import Team
from pydantic import BaseModel

user_router = APIRouter()


class InviteCreate(BaseModel):
    team_id: int
    user_id: int


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


class InviteRead(BaseModel):
    id: int
    team_id: int
    user_id: int


# GET-запрос /user/{userId}/getUser (get user by user id)
@user_router.get("/user/{user_id}/getUser", response_model=UserRead)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# GET-запрос /user/{userId}/AllInvite (все заявки пользователя)
@user_router.get("/user/{user_id}/AllInvite", response_model=List[InviteRead])
async def get_all_invites(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Invite).filter(Invite.user_id == user_id))
    invites = result.scalars().all()
    return invites


# POST-запрос /user/{teamId}/sendInvite (отправляем заявку в команду)
@user_router.post("/user/{team_id}/sendInvite", response_model=InviteRead)
async def send_invite(team_id: int, invite: InviteCreate, db: AsyncSession = Depends(get_session)):
    # Check if the team exists
    result = await db.execute(select(Team).filter(Team.id == team_id))
    team = result.scalar_one_or_none()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    # Create and save the new invite
    db_invite = Invite(
        team_id=team_id,
        user_id=invite.user_id
    )
    db.add(db_invite)
    await db.commit()
    await db.refresh(db_invite)
    return db_invite
