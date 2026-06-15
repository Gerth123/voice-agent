from fastapi import APIRouter

from app.models.enums import BookingMode
from app.schemas.user_settings import UserSettingsResponse, UserSettingsUpdate

router = APIRouter(prefix="/user-settings")


@router.get("/me", response_model=UserSettingsResponse)
async def get_my_user_settings() -> UserSettingsResponse:
    return UserSettingsResponse(
        id="settings_dev",
        assistant_display_name="KI-Assistent von Robin Gerth",
        ai_disclosure_text="Hallo, ich bin der KI-Assistent von Robin Gerth.",
        booking_mode=BookingMode.AUTO_BOOK_CLEAR_SLOTS,
        default_appointment_duration_minutes=30,
        working_hours_json={
            "monday": [{"start": "09:00", "end": "17:00"}],
            "tuesday": [{"start": "09:00", "end": "17:00"}],
            "wednesday": [{"start": "09:00", "end": "17:00"}],
            "thursday": [{"start": "09:00", "end": "17:00"}],
            "friday": [{"start": "09:00", "end": "15:00"}],
        },
        buffer_before_minutes=0,
        buffer_after_minutes=15,
        store_audio_enabled=False,
        store_transcript_enabled=False,
        store_summary_enabled=True,
        whatsapp_notifications_enabled=True,
        whatsapp_target_configured=False,
    )


@router.patch("/me", response_model=UserSettingsResponse)
async def update_my_user_settings(payload: UserSettingsUpdate) -> UserSettingsResponse:
    current = await get_my_user_settings()
    data = current.model_dump()

    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "whatsapp_target":
            data["whatsapp_target_configured"] = bool(value)
            continue
        data[key] = value

    return UserSettingsResponse(**data)

