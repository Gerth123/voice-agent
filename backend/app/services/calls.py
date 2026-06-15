from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Call, CallSummary, CallTranscript, UserSettings
from app.models.enums import CallDirection, CallStatus
from app.schemas.calls import CallDetail, CallListItem, CallSummaryResponse, CallSummaryUpdate
from app.schemas.webhooks import InboundCallResponse, InboundCallWebhook, VoiceCallEndedWebhook, WebhookAck
from app.services.dev_context import get_or_create_dev_user


async def list_current_calls(session: AsyncSession) -> list[CallListItem]:
    user = await get_or_create_dev_user(session)
    result = await session.execute(
        select(Call).where(Call.user_id == user.id).order_by(Call.started_at.desc())
    )
    await session.commit()
    return [await to_call_list_item(session, item) for item in result.scalars().all()]


async def get_current_call(session: AsyncSession, call_id: str) -> CallDetail | None:
    user = await get_or_create_dev_user(session)
    result = await session.execute(select(Call).where(Call.id == call_id, Call.user_id == user.id))
    call = result.scalar_one_or_none()
    if call is None:
        return None
    await session.commit()
    return await to_call_detail(session, call)


async def delete_current_call(session: AsyncSession, call_id: str) -> bool:
    user = await get_or_create_dev_user(session)
    result = await session.execute(select(Call).where(Call.id == call_id, Call.user_id == user.id))
    call = result.scalar_one_or_none()
    if call is None:
        return False
    await session.delete(call)
    await session.commit()
    return True


async def clear_call_audio(session: AsyncSession, call_id: str) -> bool:
    call = await _get_dev_call_model(session, call_id)
    if call is None:
        return False
    call.audio_storage_url_encrypted = None
    call.audio_recording_enabled = False
    await session.commit()
    return True


async def clear_call_transcript(session: AsyncSession, call_id: str) -> bool:
    call = await _get_dev_call_model(session, call_id)
    if call is None:
        return False
    result = await session.execute(select(CallTranscript).where(CallTranscript.call_id == call.id))
    transcript = result.scalar_one_or_none()
    if transcript is not None:
        await session.delete(transcript)
    await session.commit()
    return True


async def get_current_call_summary(
    session: AsyncSession,
    call_id: str,
) -> CallSummaryResponse | None:
    call = await _get_dev_call_model(session, call_id)
    if call is None:
        return None
    result = await session.execute(select(CallSummary).where(CallSummary.call_id == call.id))
    summary = result.scalar_one_or_none()
    await session.commit()
    if summary is None:
        return None
    return to_call_summary_response(summary)


async def update_current_call_summary(
    session: AsyncSession,
    call_id: str,
    payload: CallSummaryUpdate,
) -> CallSummaryResponse | None:
    call = await _get_dev_call_model(session, call_id)
    if call is None:
        return None

    result = await session.execute(select(CallSummary).where(CallSummary.call_id == call.id))
    summary = result.scalar_one_or_none()
    if summary is None:
        summary = CallSummary(
            call_id=call.id,
            summary_text_encrypted=payload.summary or "",
        )
        session.add(summary)

    field_map = {
        "who": "who_encrypted",
        "what": "what_encrypted",
        "when": "when_text",
        "where": "where_encrypted",
        "summary": "summary_text_encrypted",
        "next_action": "next_action",
    }
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(summary, field_map[field], value)

    await session.commit()
    await session.refresh(summary)
    return to_call_summary_response(summary)


async def create_inbound_call(
    session: AsyncSession,
    payload: InboundCallWebhook,
) -> InboundCallResponse:
    user = await get_or_create_dev_user(session)
    settings = await _get_settings(session, user.id)

    call = Call(
        tenant_id=user.tenant_id,
        user_id=user.id,
        provider=payload.provider,
        provider_call_id=payload.provider_call_id,
        direction=CallDirection.INBOUND,
        caller_phone_hash=_hash_phone(payload.from_number),
        started_at=payload.started_at,
        status=CallStatus.RECEIVED,
        audio_recording_enabled=settings.store_audio_enabled,
    )
    session.add(call)
    await session.commit()
    await session.refresh(call)

    return InboundCallResponse(
        call_id=call.id,
        assistant_intro=settings.ai_disclosure_text,
        audio_recording_enabled=settings.store_audio_enabled,
        transcript_storage_enabled=settings.store_transcript_enabled,
    )


async def mark_provider_call_ended(
    session: AsyncSession,
    payload: VoiceCallEndedWebhook,
) -> WebhookAck:
    result = await session.execute(
        select(Call).where(
            Call.provider == payload.provider,
            Call.provider_call_id == payload.provider_call_id,
        )
    )
    call = result.scalar_one_or_none()
    if call is None:
        return WebhookAck(ok=False, message="Call not found")

    call.ended_at = payload.ended_at
    call.duration_seconds = payload.duration_seconds
    call.status = CallStatus.COMPLETED if payload.status == "completed" else CallStatus.FAILED
    await session.commit()
    return WebhookAck(ok=True, message=f"Call ended event accepted for {payload.provider_call_id}")


async def _get_dev_call_model(session: AsyncSession, call_id: str) -> Call | None:
    user = await get_or_create_dev_user(session)
    result = await session.execute(select(Call).where(Call.id == call_id, Call.user_id == user.id))
    return result.scalar_one_or_none()


async def _get_settings(session: AsyncSession, user_id: str) -> UserSettings:
    result = await session.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    settings = result.scalar_one()
    return settings


async def to_call_list_item(session: AsyncSession, call: Call) -> CallListItem:
    summary_available, transcript_available = await _call_artifacts_available(session, call.id)
    return CallListItem(
        id=call.id,
        created_at=call.created_at,
        updated_at=call.updated_at,
        direction=call.direction,
        caller_phone=None,
        started_at=call.started_at,
        duration_seconds=call.duration_seconds,
        status=call.status,
        audio_recording_enabled=call.audio_recording_enabled,
        summary_available=summary_available,
        transcript_available=transcript_available,
    )


async def to_call_detail(session: AsyncSession, call: Call) -> CallDetail:
    base = await to_call_list_item(session, call)
    return CallDetail(
        **base.model_dump(),
        provider=call.provider,
        provider_call_id=call.provider_call_id,
        ended_at=call.ended_at,
        ai_disclosure_played_at=call.ai_disclosure_played_at,
        audio_delete_at=call.audio_delete_at,
        transcript_delete_at=call.transcript_delete_at,
        summary_delete_at=call.summary_delete_at,
    )


def to_call_summary_response(summary: CallSummary) -> CallSummaryResponse:
    return CallSummaryResponse(
        id=summary.id,
        created_at=summary.created_at,
        updated_at=summary.updated_at,
        call_id=summary.call_id,
        who=summary.who_encrypted,
        what=summary.what_encrypted,
        when=summary.when_text,
        where=summary.where_encrypted,
        summary=summary.summary_text_encrypted,
        next_action=summary.next_action,
        confidence_score=summary.confidence_score,
        delete_at=summary.delete_at,
    )


async def _call_artifacts_available(session: AsyncSession, call_id: str) -> tuple[bool, bool]:
    summary_result = await session.execute(select(CallSummary.id).where(CallSummary.call_id == call_id))
    transcript_result = await session.execute(
        select(CallTranscript.id).where(CallTranscript.call_id == call_id)
    )
    return summary_result.scalar_one_or_none() is not None, transcript_result.scalar_one_or_none() is not None


def _hash_phone(phone_number: str) -> str:
    normalized = "".join(character for character in phone_number if character.isdigit() or character == "+")
    return sha256(normalized.encode("utf-8")).hexdigest()

