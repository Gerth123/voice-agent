from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class MemoryEntry(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "memory_entries"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    source_type: Mapped[str] = mapped_column(String(80), nullable=False)
    source_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    content_encrypted: Mapped[str] = mapped_column(String(4096), nullable=False)
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    importance: Mapped[int] = mapped_column(default=1, nullable=False)
    valid_from: Mapped[datetime | None] = mapped_column(nullable=True)
    valid_until: Mapped[datetime | None] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

