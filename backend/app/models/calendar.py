from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin
from app.models.enums import CalendarMode, CalendarProvider


class CalendarConnection(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "calendar_connections"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    provider: Mapped[CalendarProvider] = mapped_column(Enum(CalendarProvider), nullable=False)
    mode: Mapped[CalendarMode] = mapped_column(Enum(CalendarMode), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    last_sync_at: Mapped[datetime | None] = mapped_column(nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    ical_connection = relationship("IcalConnection", back_populates="calendar_connection", uselist=False)


class IcalConnection(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ical_connections"

    calendar_connection_id: Mapped[str] = mapped_column(
        ForeignKey("calendar_connections.id"),
        unique=True,
        index=True,
        nullable=False,
    )
    ics_url_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    caldav_url_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    username_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    password_secret_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    calendar_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    supports_write: Mapped[bool] = mapped_column(default=False, nullable=False)

    calendar_connection = relationship("CalendarConnection", back_populates="ical_connection")
