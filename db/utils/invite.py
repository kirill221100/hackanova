from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.models.invite import Invite, InviteStatus
from fastapi import HTTPException


async def get_invites_by_team_id(team_id: int, session: AsyncSession):
    return (await session.execute(
        select(Invite).filter_by(team_id=team_id).options(selectinload(Invite.user)))
            ).scalar_one_or_none()


async def get_invite(team_id: int, user_id: int, session: AsyncSession):
    return (await session.execute(select(Invite).filter_by(team_id=team_id, user_id=user_id))).scalar_one_or_none()


async def accept_invite(team_id: int, user_id: int, session: AsyncSession):
    invite = await get_invite(team_id, user_id, session)
    invite.status = InviteStatus.ACCEPT.value
    await session.commit()
    return {'message': 'accept'}


async def reject_invite(team_id: int, user_id: int, session: AsyncSession):
    invite = await get_invite(team_id, user_id, session)
    invite.status = InviteStatus.REJECT.value
    await session.commit()
    return {'message': 'reject'}
