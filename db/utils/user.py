from typing import List

from fastapi import APIRouter

router = APIRouter()


@router.get('/users')
async def get_users():
    users = await get_users()
    return users
