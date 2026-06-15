from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin
from app.models.enums import NotificationChannel, NotificationStatus


class Notification(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "notifications"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    call_id: Mapped[str | None] = mapped_column(ForeignKey("calls.id"), index=True, nullable=True)
    channel: Mapped[NotificationChannel] = mapped_column(Enum(NotificationChannel), nullable=False)
    recipient_encrypted: Mapped[str] = mapped_column(String(2048), nullable=False)
    payload_json_encrypted: Mapped[str] = mapped_column(String(4096), nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus),
        default=NotificationStatus.PENDING,
        nullable=False,
    )
    provider_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(nullable=True)

    call = relationship("Call", back_populates="notifications")

