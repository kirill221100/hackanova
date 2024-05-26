from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from db.utils.team import get_team_by_id_with_users_and_tags, get_team_desc_and_tags, set_team_desc_and_tags, create_team, get_all_teams_with_users_and_tags
from db.utils.invite import create_invite, accept_invite, reject_invite, get_invitations
from schemes.team import TeamSearchResponseScheme, TeamResponseScheme, TeamSearchScheme, TeamCreateScheme, TeamCreateResponseScheme
from schemes.invite import InviteResponseScheme, AcceptInviteScheme, RejectInviteScheme, CreateInviteScheme, UserInviteResponseScheme
from db.models.invite import InviteType
from typing import List, Optional


team_router = APIRouter()


@team_router.get('/{team_id}/getTeam', response_model=TeamResponseScheme)
async def get_team_by_id_path(team_id: int, session: AsyncSession = Depends(get_session)):
    return await get_team_by_id_with_users_and_tags(team_id, session)


@team_router.get("/get-all-teams", response_model=List[TeamResponseScheme])
async def get_all_teams_path(session: AsyncSession = Depends(get_session)):
    return await get_all_teams_with_users_and_tags(session)


@team_router.get('/{team_id}/search', response_model=TeamSearchResponseScheme)
async def get_team_desc_and_tags_path(team_id: int, session: AsyncSession = Depends(get_session)):
    return await get_team_desc_and_tags(team_id, session)


@team_router.post('/{team_id}/search', response_model=dict)
async def set_team_desc_and_tags_path(team_id: int, data: TeamSearchScheme, session: AsyncSession = Depends(get_session)):
    return await set_team_desc_and_tags(team_id, data, session)


@team_router.get('/{team_id}/get-invitations-from-user', response_model=List[InviteResponseScheme])
async def get_invitations_path(team_id: int, session: AsyncSession = Depends(get_session)):
    """приглашения от юзеров команде"""
    return await get_invitations(InviteType.TO_TEAM, session, team_id=team_id)


@team_router.get("/{team_id}/get-invitations-from-team", response_model=List[InviteResponseScheme])
async def all_invitations_from_team_path(team_id: int, session: AsyncSession = Depends(get_session)):
    """приглашения отправленные из команды"""
    return await get_invitations(InviteType.TO_USER, session, team_id=team_id)


@team_router.post("/send-invite", response_model=dict)
async def send_invite_path(data: CreateInviteScheme, session: AsyncSession = Depends(get_session)):
    """отправить приглашение юзеру"""
    return await create_invite(InviteType.TO_USER, data, session)


@team_router.patch('/accept-invite', response_model=dict)
async def accept_invite_path(data: AcceptInviteScheme, session: AsyncSession = Depends(get_session)):
    """принять приглашение от юзера"""
    return await accept_invite(InviteType.TO_TEAM, data, session)


@team_router.patch('/reject-invite', response_model=dict)
async def reject_invite_path(data: RejectInviteScheme, session: AsyncSession = Depends(get_session)):
    """отклонить приглашение от юзера"""
    return await reject_invite(InviteType.TO_TEAM, data, session)


@team_router.post('/create-team', response_model=TeamCreateResponseScheme)
async def create_team_path(data: TeamCreateScheme, session: AsyncSession = Depends(get_session)):
    """только для тестов, не прод"""
    return await create_team(data, session)
