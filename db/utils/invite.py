from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.models.invite import Invite, InviteStatus, InviteType
from db.utils.user import get_user_by_id
from db.utils.team import get_team_by_id
from fastapi import HTTPException
from schemes.invite import CreateInviteScheme, AcceptInviteScheme, RejectInviteScheme
from typing import Optional


async def get_invitations_by_team_id(team_id: int, session: AsyncSession):
    return (await session.execute(
        select(Invite).filter_by(team_id=team_id).options(selectinload(Invite.user)))
            ).scalars().all()


async def get_invitations_by_user_id(user_id: int, session: AsyncSession):
    return (await session.execute(
        select(Invite).filter_by(user_id=user_id))).scalars().all()


async def get_invitations(invite_type: InviteType, session: AsyncSession, team_id: Optional[int] = None,
                          user_id: Optional[int] = None):
    filter_type = None
    if user_id:
        filter_type = (Invite.user_id == user_id)
    elif team_id:
        filter_type = (Invite.team_id == team_id)
    return (await session.execute(select(Invite).filter(filter_type & (Invite.type == invite_type)).options(selectinload(Invite.user)))).scalars().all()


async def get_invite(invite_type: InviteType, team_id: int, user_id: int, session: AsyncSession):
    return (await session.execute(
        select(Invite).filter_by(team_id=team_id, user_id=user_id, type=invite_type))).scalar_one_or_none()


async def create_invite(invite_type: InviteType, data: CreateInviteScheme, session: AsyncSession):
    if not await get_invite(invite_type, data.team_id, data.user_id, session):
        invite = Invite(type=invite_type)
        for k, v in data:
            setattr(invite, k, v)
        session.add(invite)
        await session.commit()
        return {'message': 'create'}
    raise HTTPException(409, 'Такое приглашение уже есть')


async def accept_invite(invite_type: InviteType, data: AcceptInviteScheme, session: AsyncSession):
    invite = await get_invite(invite_type, data.team_id, data.user_id, session)
    invite.status = InviteStatus.ACCEPT
    user = await get_user_by_id(data.user_id, session)
    team = await get_team_by_id(data.team_id, session)
    if user not in team.participants:
        team.participants.append(user)
    await session.commit()
    return {'message': 'accept'}


async def reject_invite(invite_type: InviteType, data: RejectInviteScheme, session: AsyncSession):
    invite = await get_invite(invite_type, data.team_id, data.user_id, session)
    invite.status = InviteStatus.REJECT
    await session.commit()
    return {'message': 'reject'}
