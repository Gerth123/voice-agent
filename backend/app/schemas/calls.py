from datetime import datetime

from app.models.enums import CallDirection, CallStatus
from app.schemas.base import ApiModel, TimestampedResponse


class CallListItem(TimestampedResponse):
    direction: CallDirection
    caller_phone: str | None = None
    started_at: datetime
    duration_seconds: int | None = None
    status: CallStatus
    audio_recording_enabled: bool
    summary_available: bool
    transcript_available: bool


class CallDetail(CallListItem):
    provider: str
    provider_call_id: str
    ended_at: datetime | None = None
    ai_disclosure_played_at: datetime | None = None
    audio_delete_at: datetime | None = None
    transcript_delete_at: datetime | None = None
    summary_delete_at: datetime | None = None


class CallSummaryResponse(TimestampedResponse):
    call_id: str
    who: str | None = None
    what: str | None = None
    when: str | None = None
    where: str | None = None
    summary: str
    next_action: str | None = None
    confidence_score: float | None = None
    delete_at: datetime | None = None


class CallSummaryUpdate(ApiModel):
    who: str | None = None
    what: str | None = None
    when: str | None = None
    where: str | None = None
    summary: str | None = None
    next_action: str | None = None

