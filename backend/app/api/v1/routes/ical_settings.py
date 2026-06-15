from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.calendar import (
    CalendarTestResponse,
    IcalSettingsCreate,
    IcalSettingsResponse,
    IcalSettingsUpdate,
)
from app.services.calendar_connections import (
    create_current_ical_settings,
    list_current_ical_settings,
    test_current_ical_settings,
    update_current_ical_settings,
)

router = APIRouter(prefix="/ical-settings")


@router.get("", response_model=list[IcalSettingsResponse])
async def list_ical_settings(
    session: AsyncSession = Depends(get_db),
) -> list[IcalSettingsResponse]:
    return await list_current_ical_settings(session)


@router.post("", response_model=IcalSettingsResponse, status_code=201)
async def create_ical_settings(
    payload: IcalSettingsCreate,
    session: AsyncSession = Depends(get_db),
) -> IcalSettingsResponse:
    settings = await create_current_ical_settings(session, payload)
    if settings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    return settings


@router.patch("/{settings_id}", response_model=IcalSettingsResponse)
async def update_ical_settings(
    settings_id: str,
    payload: IcalSettingsUpdate,
    session: AsyncSession = Depends(get_db),
) -> IcalSettingsResponse:
    settings = await update_current_ical_settings(session, settings_id, payload)
    if settings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="iCal settings not found")
    return settings


@router.post("/{settings_id}/test-read", response_model=CalendarTestResponse)
async def test_ical_read(
    settings_id: str,
    session: AsyncSession = Depends(get_db),
) -> CalendarTestResponse:
    result = await test_current_ical_settings(session, settings_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="iCal settings not found")
    return result


@router.post("/{settings_id}/test-write", response_model=CalendarTestResponse)
async def test_ical_write(
    settings_id: str,
    session: AsyncSession = Depends(get_db),
) -> CalendarTestResponse:
    result = await test_current_ical_settings(session, settings_id, write=True)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="iCal settings not found")
    return result
