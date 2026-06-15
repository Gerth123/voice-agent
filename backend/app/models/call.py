from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin
from app.db.types import enum_type
from app.models.enums import CallDirection, CallStatus


class Call(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "calls"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    contact_id: Mapped[str | None] = mapped_column(ForeignKey("contacts.id"), index=True, nullable=True)
    provider: Mapped[str] = mapped_column(String(80), nullable=False)
    provider_call_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    direction: Mapped[CallDirection] = mapped_column(enum_type(CallDirection), nullable=False)
    caller_phone_hash: Mapped[str | None] = mapped_column(String(128), index=True, nullable=True)
    caller_phone_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    started_at: Mapped[datetime] = mapped_column(index=True, nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[CallStatus] = mapped_column(enum_type(CallStatus), nullable=False)
    ai_disclosure_played_at: Mapped[datetime | None] = mapped_column(nullable=True)
    audio_recording_enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    audio_storage_url_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    audio_delete_at: Mapped[datetime | None] = mapped_column(index=True, nullable=True)
    transcript_delete_at: Mapped[datetime | None] = mapped_column(index=True, nullable=True)
    summary_delete_at: Mapped[datetime | None] = mapped_column(index=True, nullable=True)

    contact = relationship("Contact", back_populates="calls")
    summary = relationship("CallSummary", back_populates="call", uselist=False)
    transcript = relationship("CallTranscript", back_populates="call", uselist=False)
    appointment_requests = relationship("AppointmentRequest", back_populates="call")
    notifications = relationship("Notification", back_populates="call")


class CallSummary(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "call_summaries"

    call_id: Mapped[str] = mapped_column(ForeignKey("calls.id"), unique=True, index=True, nullable=False)
    who_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    what_encrypted: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    when_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    where_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    summary_text_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    next_action: Mapped[str | None] = mapped_column(String(500), nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(nullable=True)
    delete_at: Mapped[datetime | None] = mapped_column(index=True, nullable=True)

    call = relationship("Call", back_populates="summary")


class CallTranscript(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "call_transcripts"

    call_id: Mapped[str] = mapped_column(ForeignKey("calls.id"), unique=True, index=True, nullable=False)
    transcript_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    provider: Mapped[str | None] = mapped_column(String(80), nullable=True)
    delete_at: Mapped[datetime | None] = mapped_column(index=True, nullable=True)

    call = relationship("Call", back_populates="transcript")
