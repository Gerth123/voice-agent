from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin
from app.models.enums import ContactSource, DataSubjectType


class Contact(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "contacts"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    name_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    phone_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    phone_hash: Mapped[str | None] = mapped_column(String(128), index=True, nullable=True)
    email_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    company_encrypted: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    source: Mapped[ContactSource] = mapped_column(Enum(ContactSource), nullable=False)
    data_subject_type: Mapped[DataSubjectType] = mapped_column(Enum(DataSubjectType), nullable=False)
    notes_encrypted: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    calls = relationship("Call", back_populates="contact")

