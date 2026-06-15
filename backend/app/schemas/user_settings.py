from app.models.enums import BookingMode
from app.schemas.base import ApiModel, TimestampedResponse


class UserSettingsResponse(TimestampedResponse):
    assistant_display_name: str
    ai_disclosure_text: str
    booking_mode: BookingMode
    default_appointment_duration_minutes: int
    working_hours_json: dict | None = None
    buffer_before_minutes: int
    buffer_after_minutes: int
    store_audio_enabled: bool
    store_transcript_enabled: bool
    store_summary_enabled: bool
    whatsapp_notifications_enabled: bool
    whatsapp_target_configured: bool


class UserSettingsUpdate(ApiModel):
    assistant_display_name: str | None = None
    ai_disclosure_text: str | None = None
    booking_mode: BookingMode | None = None
    default_appointment_duration_minutes: int | None = None
    working_hours_json: dict | None = None
    buffer_before_minutes: int | None = None
    buffer_after_minutes: int | None = None
    store_audio_enabled: bool | None = None
    store_transcript_enabled: bool | None = None
    store_summary_enabled: bool | None = None
    whatsapp_notifications_enabled: bool | None = None
    whatsapp_target: str | None = None

