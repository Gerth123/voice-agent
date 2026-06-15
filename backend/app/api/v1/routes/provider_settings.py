from fastapi import APIRouter, HTTPException, status

from app.models.enums import ProviderDpaStatus
from app.schemas.provider_settings import (
    ProviderConfigCreate,
    ProviderConfigResponse,
    ProviderConfigUpdate,
    ProviderTestResponse,
)

router = APIRouter(prefix="/provider-settings")
PROVIDER_TYPES = {"voice", "tts", "stt", "llm"}


def _validate_provider_type(provider_type: str) -> None:
    if provider_type not in PROVIDER_TYPES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider type not found")


def _demo_provider(provider_type: str) -> ProviderConfigResponse:
    return ProviderConfigResponse(
        id=f"{provider_type}_provider_dev",
        provider_name=f"mock_{provider_type}",
        enabled=True,
        data_region="eu",
        dpa_status=ProviderDpaStatus.UNKNOWN,
        secret_configured=False,
    )


@router.get("/{provider_type}", response_model=list[ProviderConfigResponse])
async def list_provider_configs(provider_type: str) -> list[ProviderConfigResponse]:
    _validate_provider_type(provider_type)
    return [_demo_provider(provider_type)]


@router.post("/{provider_type}", response_model=ProviderConfigResponse, status_code=201)
async def create_provider_config(
    provider_type: str,
    payload: ProviderConfigCreate,
) -> ProviderConfigResponse:
    _validate_provider_type(provider_type)
    return ProviderConfigResponse(
        id=f"{provider_type}_provider_dev",
        provider_name=payload.provider_name,
        enabled=payload.enabled,
        data_region=payload.data_region,
        dpa_status=payload.dpa_status,
        secret_configured=bool(payload.secret_ref),
    )


@router.patch("/{provider_type}/{config_id}", response_model=ProviderConfigResponse)
async def update_provider_config(
    provider_type: str,
    config_id: str,
    payload: ProviderConfigUpdate,
) -> ProviderConfigResponse:
    _validate_provider_type(provider_type)
    if config_id != f"{provider_type}_provider_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider config not found")

    current = _demo_provider(provider_type).model_dump()
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "secret_ref":
            current["secret_configured"] = bool(value)
            continue
        if key == "config":
            continue
        current[key] = value
    return ProviderConfigResponse(**current)


@router.post("/{provider_type}/{config_id}/test", response_model=ProviderTestResponse)
async def test_provider_config(provider_type: str, config_id: str) -> ProviderTestResponse:
    _validate_provider_type(provider_type)
    if config_id != f"{provider_type}_provider_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider config not found")
    return ProviderTestResponse(ok=True, message=f"{provider_type} provider test placeholder succeeded")

