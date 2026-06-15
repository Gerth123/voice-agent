from fastapi import APIRouter

from app.schemas.webhooks import (
    InboundCallResponse,
    InboundCallWebhook,
    NotificationStatusWebhook,
    VoiceCallEndedWebhook,
    WebhookAck,
)

router = APIRouter(prefix="/webhooks")


@router.post("/voice/inbound-call", response_model=InboundCallResponse)
async def handle_inbound_call(payload: InboundCallWebhook) -> InboundCallResponse:
    return InboundCallResponse(
        call_id=f"call_{payload.provider_call_id}",
        assistant_intro="Hallo, ich bin der KI-Assistent von Robin Gerth.",
        audio_recording_enabled=False,
        transcript_storage_enabled=False,
    )


@router.post("/voice/call-ended", response_model=WebhookAck)
async def handle_call_ended(payload: VoiceCallEndedWebhook) -> WebhookAck:
    return WebhookAck(
        ok=True,
        message=f"Call ended event accepted for {payload.provider_call_id}",
    )


@router.post("/n8n/notification-status", response_model=WebhookAck)
async def handle_notification_status(payload: NotificationStatusWebhook) -> WebhookAck:
    return WebhookAck(
        ok=True,
        message=f"Notification status accepted for {payload.notification_id}",
    )

