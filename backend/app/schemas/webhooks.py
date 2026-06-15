from datetime import datetime

from app.models.enums import NotificationStatus
from app.schemas.base import ApiModel


class InboundCallWebhook(ApiModel):
    provider: str
    provider_call_id: str
    from_number: str
    to_number: str
    started_at: datetime


class InboundCallResponse(ApiModel):
    call_id: str
    assistant_intro: str
    audio_recording_enabled: bool
    transcript_storage_enabled: bool


class VoiceCallEndedWebhook(ApiModel):
    provider: str
    provider_call_id: str
    ended_at: datetime
    duration_seconds: int | None = None
    status: str = "completed"


class NotificationStatusWebhook(ApiModel):
    notification_id: str
    status: NotificationStatus
    provider_message_id: str | None = None
    sent_at: datetime | None = None


class WebhookAck(ApiModel):
    ok: bool
    message: str

