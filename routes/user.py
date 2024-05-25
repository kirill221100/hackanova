from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session
from schemes.user import UserResponse

user_router = APIRouter()

