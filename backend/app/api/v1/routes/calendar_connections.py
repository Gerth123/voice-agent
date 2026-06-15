from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.calendar import (
    CalendarConnectionCreate,
    CalendarConnectionResponse,
    CalendarConnectionUpdate,
    CalendarTestResponse,
)
from app.services.calendar_connections import (
    create_current_calendar_connection,
    get_current_calendar_connection,
    list_current_calendar_connections,
    test_current_calendar_connection,
    to_calendar_connection_response,
    update_current_calendar_connection,
)

router = APIRouter(prefix="/calendar-connections")


@router.get("", response_model=list[CalendarConnectionResponse])
async def list_calendar_connections(
    session: AsyncSession = Depends(get_db),
) -> list[CalendarConnectionResponse]:
    return await list_current_calendar_connections(session)


@router.post("", response_model=CalendarConnectionResponse, status_code=201)
async def create_calendar_connection(
    payload: CalendarConnectionCreate,
    session: AsyncSession = Depends(get_db),
) -> CalendarConnectionResponse:
    return await create_current_calendar_connection(session, payload)


@router.get("/{connection_id}", response_model=CalendarConnectionResponse)
async def get_calendar_connection(
    connection_id: str,
    session: AsyncSession = Depends(get_db),
) -> CalendarConnectionResponse:
    connection = await get_current_calendar_connection(session, connection_id)
    if connection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    return to_calendar_connection_response(connection)


@router.patch("/{connection_id}", response_model=CalendarConnectionResponse)
async def update_calendar_connection(
    connection_id: str,
    payload: CalendarConnectionUpdate,
    session: AsyncSession = Depends(get_db),
) -> CalendarConnectionResponse:
    connection = await update_current_calendar_connection(session, connection_id, payload)
    if connection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    return connection


@router.post("/{connection_id}/test", response_model=CalendarTestResponse)
async def test_calendar_connection(
    connection_id: str,
    session: AsyncSession = Depends(get_db),
) -> CalendarTestResponse:
    result = await test_current_calendar_connection(session, connection_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    return result


@router.post("/{connection_id}/sync", response_model=CalendarTestResponse)
async def sync_calendar_connection(
    connection_id: str,
    session: AsyncSession = Depends(get_db),
) -> CalendarTestResponse:
    result = await test_current_calendar_connection(session, connection_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    return CalendarTestResponse(ok=True, message="Calendar sync placeholder queued")
