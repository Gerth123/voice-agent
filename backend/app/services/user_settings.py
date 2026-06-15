from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, UserSettings
from app.schemas.user_settings import UserSettingsResponse, UserSettingsUpdate
from app.services.dev_context import get_or_create_dev_user

WHATSAPP_CONFIGURED_MARKER = "__configured__"


async def get_current_user_settings(session: AsyncSession) -> UserSettingsResponse:
    user = await get_or_create_dev_user(session)
    settings = await _get_settings_for_user(session, user)
    await session.commit()
    return to_user_settings_response(settings)


async def update_current_user_settings(
    session: AsyncSession,
    payload: UserSettingsUpdate,
) -> UserSettingsResponse:
    user = await get_or_create_dev_user(session)
    settings = await _get_settings_for_user(session, user)

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "whatsapp_target":
            settings.whatsapp_target_encrypted = WHATSAPP_CONFIGURED_MARKER if value else None
            continue
        setattr(settings, field, value)

    await session.commit()
    await session.refresh(settings)
    return to_user_settings_response(settings)


async def _get_settings_for_user(session: AsyncSession, user: User) -> UserSettings:
    result = await session.execute(select(UserSettings).where(UserSettings.user_id == user.id))
    settings = result.scalar_one_or_none()
    if settings is None:
        raise RuntimeError("Dev user settings were not initialized")
    return settings


def to_user_settings_response(settings: UserSettings) -> UserSettingsResponse:
    return UserSettingsResponse(
        id=settings.id,
        created_at=settings.created_at,
        updated_at=settings.updated_at,
        assistant_display_name=settings.assistant_display_name,
        ai_disclosure_text=settings.ai_disclosure_text,
        booking_mode=settings.booking_mode,
        default_appointment_duration_minutes=settings.default_appointment_duration_minutes,
        working_hours_json=settings.working_hours_json,
        buffer_before_minutes=settings.buffer_before_minutes,
        buffer_after_minutes=settings.buffer_after_minutes,
        store_audio_enabled=settings.store_audio_enabled,
        store_transcript_enabled=settings.store_transcript_enabled,
        store_summary_enabled=settings.store_summary_enabled,
        whatsapp_notifications_enabled=settings.whatsapp_notifications_enabled,
        whatsapp_target_configured=bool(settings.whatsapp_target_encrypted),
    )
