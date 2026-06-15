from datetime import datetime

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin
from app.db.types import enum_type
from app.models.enums import UserRole


class User(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(enum_type(UserRole), default=UserRole.OWNER, nullable=False)
    timezone: Mapped[str] = mapped_column(String(80), default="Europe/Berlin", nullable=False)
    locale: Mapped[str] = mapped_column(String(20), default="de-DE", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    tenant = relationship("Tenant", back_populates="users")
    settings = relationship("UserSettings", back_populates="user", uselist=False)


class UserSettings(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user_settings"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, index=True, nullable=False)
    assistant_display_name: Mapped[str] = mapped_column(
        String(255),
        default="KI-Assistent von Robin Gerth",
        nullable=False,
    )
    ai_disclosure_text: Mapped[str] = mapped_column(
        String(500),
        default="Hallo, ich bin der KI-Assistent von Robin Gerth.",
        nullable=False,
    )
    booking_mode: Mapped[str] = mapped_column(
        String(50),
        default="auto_book_clear_slots",
        nullable=False,
    )
    default_appointment_duration_minutes: Mapped[int] = mapped_column(default=30, nullable=False)
    working_hours_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    buffer_before_minutes: Mapped[int] = mapped_column(default=0, nullable=False)
    buffer_after_minutes: Mapped[int] = mapped_column(default=15, nullable=False)
    store_audio_enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    store_transcript_enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    store_summary_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    whatsapp_notifications_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    whatsapp_target_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    user = relationship("User", back_populates="settings")
