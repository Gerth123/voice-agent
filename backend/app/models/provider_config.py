from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin
from app.models.enums import ProviderDpaStatus


class ProviderConfigMixin(UuidPrimaryKeyMixin, TimestampMixin):
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    provider_name: Mapped[str] = mapped_column(String(120), nullable=False)
    enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    config_json_encrypted: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    secret_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    data_region: Mapped[str | None] = mapped_column(String(80), nullable=True)
    dpa_status: Mapped[ProviderDpaStatus] = mapped_column(
        Enum(ProviderDpaStatus),
        default=ProviderDpaStatus.UNKNOWN,
        nullable=False,
    )


class VoiceProviderConfig(ProviderConfigMixin, Base):
    __tablename__ = "voice_provider_configs"


class TtsProviderConfig(ProviderConfigMixin, Base):
    __tablename__ = "tts_provider_configs"


class SttProviderConfig(ProviderConfigMixin, Base):
    __tablename__ = "stt_provider_configs"


class LlmProviderConfig(ProviderConfigMixin, Base):
    __tablename__ = "llm_provider_configs"

