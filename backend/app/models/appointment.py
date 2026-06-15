from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin
from app.models.enums import AppointmentRequestStatus, AppointmentStatus


class AppointmentRequest(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "appointment_requests"

    call_id: Mapped[str] = mapped_column(ForeignKey("calls.id"), index=True, nullable=False)
    contact_id: Mapped[str | None] = mapped_column(ForeignKey("contacts.id"), index=True, nullable=True)
    requested_time_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    requested_location_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    topic_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[AppointmentRequestStatus] = mapped_column(
        Enum(AppointmentRequestStatus),
        default=AppointmentRequestStatus.DETECTED,
        nullable=False,
    )
    confidence_score: Mapped[float | None] = mapped_column(nullable=True)

    call = relationship("Call", back_populates="appointment_requests")
    appointment = relationship("Appointment", back_populates="appointment_request", uselist=False)


class Appointment(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "appointments"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    appointment_request_id: Mapped[str | None] = mapped_column(
        ForeignKey("appointment_requests.id"),
        unique=True,
        index=True,
        nullable=True,
    )
    calendar_connection_id: Mapped[str | None] = mapped_column(
        ForeignKey("calendar_connections.id"),
        index=True,
        nullable=True,
    )
    external_calendar_event_id_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    title_encrypted: Mapped[str] = mapped_column(String(2048), nullable=False)
    description_encrypted: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    location_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    starts_at: Mapped[datetime] = mapped_column(index=True, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(index=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(80), default="Europe/Berlin", nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus),
        default=AppointmentStatus.PROPOSED,
        nullable=False,
    )
    created_by: Mapped[str] = mapped_column(String(50), default="agent", nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    appointment_request = relationship("AppointmentRequest", back_populates="appointment")

