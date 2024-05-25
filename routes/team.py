from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.team import get_team_by_id, get_team_desc_and_tags, set_team_desc_and_tags, create_team
from db.utils.invite import get_invitations_by_team_id, accept_invite, reject_invite
from schemes.team import TeamSearchResponseScheme, TeamResponseScheme, TeamSearchScheme, TeamCreateScheme, TeamCreateResponseScheme
from schemes.invite import InviteResponseScheme, AcceptInviteScheme, RejectInviteScheme
from typing import List, Optional


team_router = APIRouter()


@team_router.get('/{team_id}/getTeam', response_model=TeamResponseScheme)
async def get_team_by_id_path(team_id: int, session: AsyncSession = Depends(get_session)):
    return await get_team_by_id(team_id, session)


@team_router.get('/{team_id}/search', response_model=TeamSearchResponseScheme)
async def get_team_desc_and_tags_path(team_id: int, session: AsyncSession = Depends(get_session)):
    return await get_team_desc_and_tags(team_id, session)


@team_router.post('/{team_id}/search', response_model=dict)
async def set_team_desc_and_tags_path(team_id: int, data: TeamSearchScheme, session: AsyncSession = Depends(get_session)):
    return await set_team_desc_and_tags(team_id, data, session)


@team_router.get('/{team_id}/get-invitations', response_model=List[InviteResponseScheme])
async def get_invitations_path(team_id: int, session: AsyncSession = Depends(get_session)):
    return await get_invitations_by_team_id(team_id, session)


@team_router.patch('/{team_id}/accept-invite', response_model=dict)
async def accept_invite_path(team_id: int, data: AcceptInviteScheme, session: AsyncSession = Depends(get_session)):
    return await accept_invite(team_id, data, session)


@team_router.patch('/{team_id}/reject-invite', response_model=dict)
async def reject_invite_path(team_id: int, data: RejectInviteScheme, session: AsyncSession = Depends(get_session)):
    return await reject_invite(team_id, data, session)


@team_router.post('/create-team', response_model=TeamCreateResponseScheme)
async def create_team_path(data: TeamCreateScheme, session: AsyncSession = Depends(get_session)):
    return await create_team(data, session)
