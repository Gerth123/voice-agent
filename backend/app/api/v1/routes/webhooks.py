from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.webhooks import (
    InboundCallResponse,
    InboundCallWebhook,
    NotificationStatusWebhook,
    VoiceCallEndedWebhook,
    WebhookAck,
)
from app.services.calls import create_inbound_call, mark_provider_call_ended

router = APIRouter(prefix="/webhooks")


@router.post("/voice/inbound-call", response_model=InboundCallResponse)
async def handle_inbound_call(
    payload: InboundCallWebhook,
    session: AsyncSession = Depends(get_db),
) -> InboundCallResponse:
    return await create_inbound_call(session, payload)


@router.post("/voice/call-ended", response_model=WebhookAck)
async def handle_call_ended(
    payload: VoiceCallEndedWebhook,
    session: AsyncSession = Depends(get_db),
) -> WebhookAck:
    return await mark_provider_call_ended(session, payload)


@router.post("/n8n/notification-status", response_model=WebhookAck)
async def handle_notification_status(payload: NotificationStatusWebhook) -> WebhookAck:
    return WebhookAck(
        ok=True,
        message=f"Notification status accepted for {payload.notification_id}",
    )
