from datetime import datetime

from app.models.enums import AppointmentStatus
from app.schemas.base import ApiModel, TimestampedResponse


class AppointmentResponse(TimestampedResponse):
    title: str
    description: str | None = None
    location: str | None = None
    starts_at: datetime
    ends_at: datetime
    timezone: str
    status: AppointmentStatus
    created_by: str


class AppointmentCreate(ApiModel):
    title: str
    description: str | None = None
    location: str | None = None
    starts_at: datetime
    ends_at: datetime
    timezone: str = "Europe/Berlin"


class AppointmentAvailabilityRequest(ApiModel):
    starts_at: datetime
    duration_minutes: int = 30
    timezone: str = "Europe/Berlin"


class AppointmentSlot(ApiModel):
    starts_at: datetime
    ends_at: datetime


class AppointmentAvailabilityResponse(ApiModel):
    available: bool
    suggested_slots: list[AppointmentSlot]

