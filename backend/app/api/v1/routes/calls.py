from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status

from app.models.enums import CallDirection, CallStatus
from app.schemas.calls import CallDetail, CallListItem, CallSummaryResponse, CallSummaryUpdate

router = APIRouter(prefix="/calls")


def _demo_call() -> CallDetail:
    return CallDetail(
        id="call_dev",
        direction=CallDirection.INBOUND,
        caller_phone=None,
        started_at=datetime(2026, 6, 15, 9, 30, tzinfo=UTC),
        ended_at=datetime(2026, 6, 15, 9, 33, tzinfo=UTC),
        duration_seconds=186,
        status=CallStatus.COMPLETED,
        audio_recording_enabled=False,
        summary_available=True,
        transcript_available=False,
        provider="mock_voice",
        provider_call_id="provider_call_dev",
        ai_disclosure_played_at=datetime(2026, 6, 15, 9, 30, 3, tzinfo=UTC),
    )


@router.get("", response_model=list[CallListItem])
async def list_calls() -> list[CallListItem]:
    return [CallListItem(**_demo_call().model_dump())]


@router.get("/{call_id}", response_model=CallDetail)
async def get_call(call_id: str) -> CallDetail:
    if call_id != "call_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return _demo_call()


@router.delete("/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_call(call_id: str) -> None:
    if call_id != "call_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")


@router.post("/{call_id}/delete-audio", status_code=status.HTTP_204_NO_CONTENT)
async def delete_call_audio(call_id: str) -> None:
    if call_id != "call_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")


@router.post("/{call_id}/delete-transcript", status_code=status.HTTP_204_NO_CONTENT)
async def delete_call_transcript(call_id: str) -> None:
    if call_id != "call_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")


@router.get("/{call_id}/summary", response_model=CallSummaryResponse)
async def get_call_summary(call_id: str) -> CallSummaryResponse:
    if call_id != "call_dev":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")

    return CallSummaryResponse(
        id="summary_dev",
        call_id=call_id,
        who="Unbekannter Anrufer",
        what="Anfrage wurde aufgenommen",
        when="heute",
        where="nicht genannt",
        summary="Kurze strukturierte Zusammenfassung des Anrufs.",
        next_action="WhatsApp-Benachrichtigung senden",
        confidence_score=0.9,
    )


@router.patch("/{call_id}/summary", response_model=CallSummaryResponse)
async def update_call_summary(call_id: str, payload: CallSummaryUpdate) -> CallSummaryResponse:
    current = await get_call_summary(call_id)
    data = current.model_dump()
    data.update(payload.model_dump(exclude_unset=True))
    return CallSummaryResponse(**data)

