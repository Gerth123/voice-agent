from datetime import datetime

from app.models.enums import CalendarMode, CalendarProvider
from app.schemas.base import ApiModel, TimestampedResponse


class CalendarConnectionResponse(TimestampedResponse):
    provider: CalendarProvider
    mode: CalendarMode
    status: str
    display_name: str | None = None
    last_sync_at: datetime | None = None


class CalendarConnectionCreate(ApiModel):
    provider: CalendarProvider
    mode: CalendarMode
    display_name: str | None = None


class CalendarConnectionUpdate(ApiModel):
    mode: CalendarMode | None = None
    status: str | None = None
    display_name: str | None = None


class IcalSettingsResponse(TimestampedResponse):
    calendar_connection_id: str
    calendar_name: str | None = None
    has_ics_url: bool
    has_caldav_url: bool
    has_username: bool
    supports_write: bool


class IcalSettingsCreate(ApiModel):
    calendar_connection_id: str
    ics_url: str | None = None
    caldav_url: str | None = None
    username: str | None = None
    password: str | None = None
    calendar_name: str | None = None
    supports_write: bool = False


class IcalSettingsUpdate(ApiModel):
    ics_url: str | None = None
    caldav_url: str | None = None
    username: str | None = None
    password: str | None = None
    calendar_name: str | None = None
    supports_write: bool | None = None


class CalendarTestResponse(ApiModel):
    ok: bool
    message: str

