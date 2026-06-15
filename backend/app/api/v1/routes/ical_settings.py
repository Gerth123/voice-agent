from fastapi import APIRouter, HTTPException, status

from app.schemas.calendar import (
    CalendarTestResponse,
    IcalSettingsCreate,
    IcalSettingsResponse,
    IcalSettingsUpdate,
)

router = APIRouter(prefix="/ical-settings")


def _demo_ical_settings() -> IcalSettingsResponse:
    return IcalSettingsResponse(
        id="ical_dev",
        calendar_connection_id="calendar_dev",
        calendar_name="Robin iPhone Kalender",
        has_ics_url=True,
        has_caldav_url=False,
        has_username=False,
        supports_write=False,
    )


@router.get("", response_model=list[IcalSettingsResponse])
async def list_ical_settings() -> list[IcalSettingsResponse]:
    return [_demo_ical_settings()]


@router.post("", response_model=IcalSettingsResponse, status_code=201)
async def create_ical_settings(payload: IcalSettingsCreate) -> IcalSettingsResponse:
    return IcalSettingsResponse(
        id="ical_dev",
        calendar_connection_id=payload.calendar_connection_id,
        calendar_name=payload.calendar_name,
        has_ics_url=bool(payload.ics_url),
        has_caldav_url=bool(payload.caldav_url),
        has_username=bool(payload.username),
        supports_write=payload.supports_write,
    )


@router.patch("/{settings_id}", response_model=IcalSettingsResponse)
async def update_ical_settings(
    settings_id: str,
    payload: IcalSettingsUpdate,
) -> IcalSettingsResponse:
    if settings_id != "ical_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="iCal settings not found")

    current = _demo_ical_settings().model_dump()
    current["has_ics_url"] = bool(payload.ics_url) if payload.ics_url is not None else current["has_ics_url"]
    current["has_caldav_url"] = (
        bool(payload.caldav_url) if payload.caldav_url is not None else current["has_caldav_url"]
    )
    current["has_username"] = (
        bool(payload.username) if payload.username is not None else current["has_username"]
    )
    current["supports_write"] = (
        payload.supports_write if payload.supports_write is not None else current["supports_write"]
    )
    current["calendar_name"] = payload.calendar_name or current["calendar_name"]
    return IcalSettingsResponse(**current)


@router.post("/{settings_id}/test-read", response_model=CalendarTestResponse)
async def test_ical_read(settings_id: str) -> CalendarTestResponse:
    if settings_id != "ical_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="iCal settings not found")
    return CalendarTestResponse(ok=True, message="iCal read test placeholder succeeded")


@router.post("/{settings_id}/test-write", response_model=CalendarTestResponse)
async def test_ical_write(settings_id: str) -> CalendarTestResponse:
    if settings_id != "ical_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="iCal settings not found")
    return CalendarTestResponse(ok=False, message="CalDAV write is not configured yet")

