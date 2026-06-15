from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user_settings import UserSettingsResponse, UserSettingsUpdate
from app.services.user_settings import get_current_user_settings, update_current_user_settings

router = APIRouter(prefix="/user-settings")


@router.get("/me", response_model=UserSettingsResponse)
async def get_my_user_settings(
    session: AsyncSession = Depends(get_db),
) -> UserSettingsResponse:
    return await get_current_user_settings(session)


@router.patch("/me", response_model=UserSettingsResponse)
async def update_my_user_settings(
    payload: UserSettingsUpdate,
    session: AsyncSession = Depends(get_db),
) -> UserSettingsResponse:
    return await update_current_user_settings(session, payload)
