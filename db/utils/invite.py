from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.models.invite import Invite, InviteStatus
from db.utils.user import get_user_by_id
from db.utils.team import get_team_by_id
from fastapi import HTTPException
from schemes.invite import InviteScheme, AcceptInviteScheme, RejectInviteScheme


async def create_invite(team_id: int, data: InviteScheme, session: AsyncSession):
    invite = Invite(team_id=team_id)
    for k, v in data:
        setattr(invite, k, v)
    session.add(invite)
    await session.commit()
    return {'message': 'create'}


async def get_invitations_by_team_id(team_id: int, session: AsyncSession):
    return (await session.execute(
        select(Invite).filter_by(team_id=team_id).options(selectinload(Invite.user)))
            ).scalars().all()


async def get_invitations_by_user_id(user_id: int, session: AsyncSession):
    return (await session.execute(
        select(Invite).filter_by(user_id=user_id))).scalars().all()


async def get_invite(team_id: int, user_id: int, session: AsyncSession):
    return (await session.execute(select(Invite).filter_by(team_id=team_id, user_id=user_id))).scalar_one_or_none()


async def accept_invite(team_id: int, data: AcceptInviteScheme, session: AsyncSession):
    invite = await get_invite(team_id, data.user_id, session)
    invite.status = InviteStatus.ACCEPT
    user = await get_user_by_id(data.user_id, session)
    team = await get_team_by_id(team_id, session)
    team.participants.append(user)
    await session.commit()
    return {'message': 'accept'}


async def reject_invite(team_id: int, data: RejectInviteScheme, session: AsyncSession):
    invite = await get_invite(team_id, data.user_id, session)
    invite.status = InviteStatus.REJECT
    await session.commit()
    return {'message': 'reject'}
