from datetime import datetime

from sqlalchemy import Enum, ForeignKey, JSON, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin
from app.models.enums import (
    AuditActorType,
    ConsentEvidenceType,
    ConsentStatus,
    ConsentType,
    DeleteMode,
)


class ConsentRecord(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "consent_records"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    call_id: Mapped[str | None] = mapped_column(ForeignKey("calls.id"), index=True, nullable=True)
    contact_id: Mapped[str | None] = mapped_column(ForeignKey("contacts.id"), index=True, nullable=True)
    type: Mapped[ConsentType] = mapped_column(Enum(ConsentType), nullable=False)
    status: Mapped[ConsentStatus] = mapped_column(Enum(ConsentStatus), nullable=False)
    captured_at: Mapped[datetime] = mapped_column(nullable=False)
    evidence_type: Mapped[ConsentEvidenceType] = mapped_column(Enum(ConsentEvidenceType), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)


class RetentionPolicy(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "retention_policies"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    data_type: Mapped[str] = mapped_column(String(80), nullable=False)
    retention_days: Mapped[int] = mapped_column(nullable=False)
    delete_mode: Mapped[DeleteMode] = mapped_column(Enum(DeleteMode), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class AuditLog(UuidPrimaryKeyMixin, Base):
    __tablename__ = "audit_logs"

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    actor_type: Mapped[AuditActorType] = mapped_column(Enum(AuditActorType), nullable=False)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    metadata_redacted_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
