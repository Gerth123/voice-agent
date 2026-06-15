from datetime import timedelta

from fastapi import APIRouter

from app.models.enums import AppointmentStatus
from app.schemas.appointments import (
    AppointmentAvailabilityRequest,
    AppointmentAvailabilityResponse,
    AppointmentCreate,
    AppointmentResponse,
    AppointmentSlot,
)

router = APIRouter(prefix="/appointments")


@router.get("", response_model=list[AppointmentResponse])
async def list_appointments() -> list[AppointmentResponse]:
    return []


@router.post("", response_model=AppointmentResponse, status_code=201)
async def create_appointment(payload: AppointmentCreate) -> AppointmentResponse:
    return AppointmentResponse(
        id="appointment_dev",
        title=payload.title,
        description=payload.description,
        location=payload.location,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        timezone=payload.timezone,
        status=AppointmentStatus.BOOKED,
        created_by="agent",
    )


@router.post("/check-availability", response_model=AppointmentAvailabilityResponse)
async def check_availability(
    payload: AppointmentAvailabilityRequest,
) -> AppointmentAvailabilityResponse:
    slot = AppointmentSlot(
        starts_at=payload.starts_at,
        ends_at=payload.starts_at + timedelta(minutes=payload.duration_minutes),
    )
    return AppointmentAvailabilityResponse(available=True, suggested_slots=[slot])

