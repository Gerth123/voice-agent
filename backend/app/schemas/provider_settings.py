from app.models.enums import ProviderDpaStatus
from app.schemas.base import ApiModel, TimestampedResponse


class ProviderConfigResponse(TimestampedResponse):
    provider_name: str
    enabled: bool
    data_region: str | None = None
    dpa_status: ProviderDpaStatus
    secret_configured: bool


class ProviderConfigCreate(ApiModel):
    provider_name: str
    enabled: bool = False
    data_region: str | None = None
    config: dict | None = None
    secret_ref: str | None = None
    dpa_status: ProviderDpaStatus = ProviderDpaStatus.UNKNOWN


class ProviderConfigUpdate(ApiModel):
    enabled: bool | None = None
    data_region: str | None = None
    config: dict | None = None
    secret_ref: str | None = None
    dpa_status: ProviderDpaStatus | None = None


class ProviderTestResponse(ApiModel):
    ok: bool
    message: str

