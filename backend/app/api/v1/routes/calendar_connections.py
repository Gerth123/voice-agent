from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status

from app.schemas.calendar import (
    CalendarConnectionCreate,
    CalendarConnectionResponse,
    CalendarConnectionUpdate,
    CalendarTestResponse,
)

router = APIRouter(prefix="/calendar-connections")


def _demo_connection() -> CalendarConnectionResponse:
    return CalendarConnectionResponse(
        id="calendar_dev",
        provider="ical",
        mode="read_write",
        status="active",
        display_name="Robin iPhone Kalender",
        last_sync_at=datetime(2026, 6, 15, 10, 0, tzinfo=UTC),
    )


@router.get("", response_model=list[CalendarConnectionResponse])
async def list_calendar_connections() -> list[CalendarConnectionResponse]:
    return [_demo_connection()]


@router.post("", response_model=CalendarConnectionResponse, status_code=201)
async def create_calendar_connection(
    payload: CalendarConnectionCreate,
) -> CalendarConnectionResponse:
    return CalendarConnectionResponse(
        id="calendar_dev",
        provider=payload.provider,
        mode=payload.mode,
        status="active",
        display_name=payload.display_name,
    )


@router.get("/{connection_id}", response_model=CalendarConnectionResponse)
async def get_calendar_connection(connection_id: str) -> CalendarConnectionResponse:
    if connection_id != "calendar_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar not found")
    return _demo_connection()


@router.patch("/{connection_id}", response_model=CalendarConnectionResponse)
async def update_calendar_connection(
    connection_id: str,
    payload: CalendarConnectionUpdate,
) -> CalendarConnectionResponse:
    current = await get_calendar_connection(connection_id)
    data = current.model_dump()
    data.update(payload.model_dump(exclude_unset=True))
    return CalendarConnectionResponse(**data)


@router.post("/{connection_id}/test", response_model=CalendarTestResponse)
async def test_calendar_connection(connection_id: str) -> CalendarTestResponse:
    await get_calendar_connection(connection_id)
    return CalendarTestResponse(ok=True, message="Calendar connection test placeholder succeeded")


@router.post("/{connection_id}/sync", response_model=CalendarTestResponse)
async def sync_calendar_connection(connection_id: str) -> CalendarTestResponse:
    await get_calendar_connection(connection_id)
    return CalendarTestResponse(ok=True, message="Calendar sync placeholder queued")

