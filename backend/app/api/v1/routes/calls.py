from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.calls import CallDetail, CallListItem, CallSummaryResponse, CallSummaryUpdate
from app.services.calls import (
    clear_call_audio,
    clear_call_transcript,
    delete_current_call,
    get_current_call,
    get_current_call_summary,
    list_current_calls,
    update_current_call_summary,
)

router = APIRouter(prefix="/calls")


@router.get("", response_model=list[CallListItem])
async def list_calls(session: AsyncSession = Depends(get_db)) -> list[CallListItem]:
    return await list_current_calls(session)


@router.get("/{call_id}", response_model=CallDetail)
async def get_call(
    call_id: str,
    session: AsyncSession = Depends(get_db),
) -> CallDetail:
    call = await get_current_call(session, call_id)
    if call is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return call


@router.delete("/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_call(
    call_id: str,
    session: AsyncSession = Depends(get_db),
) -> None:
    deleted = await delete_current_call(session, call_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")


@router.post("/{call_id}/delete-audio", status_code=status.HTTP_204_NO_CONTENT)
async def delete_call_audio(
    call_id: str,
    session: AsyncSession = Depends(get_db),
) -> None:
    deleted = await clear_call_audio(session, call_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")


@router.post("/{call_id}/delete-transcript", status_code=status.HTTP_204_NO_CONTENT)
async def delete_call_transcript(
    call_id: str,
    session: AsyncSession = Depends(get_db),
) -> None:
    deleted = await clear_call_transcript(session, call_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")


@router.get("/{call_id}/summary", response_model=CallSummaryResponse)
async def get_call_summary(
    call_id: str,
    session: AsyncSession = Depends(get_db),
) -> CallSummaryResponse:
    summary = await get_current_call_summary(session, call_id)
    if summary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")
    return summary


@router.patch("/{call_id}/summary", response_model=CallSummaryResponse)
async def update_call_summary(
    call_id: str,
    payload: CallSummaryUpdate,
    session: AsyncSession = Depends(get_db),
) -> CallSummaryResponse:
    summary = await update_current_call_summary(session, call_id, payload)
    if summary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return summary
