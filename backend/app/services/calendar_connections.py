from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CalendarConnection, IcalConnection
from app.schemas.calendar import (
    CalendarConnectionCreate,
    CalendarConnectionResponse,
    CalendarConnectionUpdate,
    CalendarTestResponse,
    IcalSettingsCreate,
    IcalSettingsResponse,
    IcalSettingsUpdate,
)
from app.services.dev_context import get_or_create_dev_user

SENSITIVE_CONFIGURED_MARKER = "__configured__"


async def list_current_calendar_connections(
    session: AsyncSession,
) -> list[CalendarConnectionResponse]:
    user = await get_or_create_dev_user(session)
    result = await session.execute(
        select(CalendarConnection).where(CalendarConnection.user_id == user.id)
    )
    await session.commit()
    return [to_calendar_connection_response(item) for item in result.scalars().all()]


async def create_current_calendar_connection(
    session: AsyncSession,
    payload: CalendarConnectionCreate,
) -> CalendarConnectionResponse:
    user = await get_or_create_dev_user(session)
    connection = CalendarConnection(
        user_id=user.id,
        provider=payload.provider,
        mode=payload.mode,
        status="active",
        display_name=payload.display_name,
    )
    session.add(connection)
    await session.commit()
    await session.refresh(connection)
    return to_calendar_connection_response(connection)


async def get_current_calendar_connection(
    session: AsyncSession,
    connection_id: str,
) -> CalendarConnection | None:
    user = await get_or_create_dev_user(session)
    result = await session.execute(
        select(CalendarConnection).where(
            CalendarConnection.id == connection_id,
            CalendarConnection.user_id == user.id,
        )
    )
    return result.scalar_one_or_none()


async def update_current_calendar_connection(
    session: AsyncSession,
    connection_id: str,
    payload: CalendarConnectionUpdate,
) -> CalendarConnectionResponse | None:
    connection = await get_current_calendar_connection(session, connection_id)
    if connection is None:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(connection, field, value)

    await session.commit()
    await session.refresh(connection)
    return to_calendar_connection_response(connection)


async def test_current_calendar_connection(
    session: AsyncSession,
    connection_id: str,
) -> CalendarTestResponse | None:
    connection = await get_current_calendar_connection(session, connection_id)
    if connection is None:
        return None
    await session.commit()
    return CalendarTestResponse(ok=True, message="Calendar connection exists")


async def list_current_ical_settings(session: AsyncSession) -> list[IcalSettingsResponse]:
    user = await get_or_create_dev_user(session)
    result = await session.execute(
        select(IcalConnection)
        .join(CalendarConnection)
        .where(CalendarConnection.user_id == user.id)
    )
    await session.commit()
    return [to_ical_settings_response(item) for item in result.scalars().all()]


async def create_current_ical_settings(
    session: AsyncSession,
    payload: IcalSettingsCreate,
) -> IcalSettingsResponse | None:
    connection = await get_current_calendar_connection(session, payload.calendar_connection_id)
    if connection is None:
        return None

    settings = IcalConnection(
        calendar_connection_id=connection.id,
        ics_url_encrypted=SENSITIVE_CONFIGURED_MARKER if payload.ics_url else None,
        caldav_url_encrypted=SENSITIVE_CONFIGURED_MARKER if payload.caldav_url else None,
        username_encrypted=SENSITIVE_CONFIGURED_MARKER if payload.username else None,
        password_secret_ref=SENSITIVE_CONFIGURED_MARKER if payload.password else None,
        calendar_name=payload.calendar_name,
        supports_write=payload.supports_write,
    )
    session.add(settings)
    await session.commit()
    await session.refresh(settings)
    return to_ical_settings_response(settings)


async def update_current_ical_settings(
    session: AsyncSession,
    settings_id: str,
    payload: IcalSettingsUpdate,
) -> IcalSettingsResponse | None:
    result = await session.execute(select(IcalConnection).where(IcalConnection.id == settings_id))
    settings = result.scalar_one_or_none()
    if settings is None:
        return None

    if payload.ics_url is not None:
        settings.ics_url_encrypted = SENSITIVE_CONFIGURED_MARKER if payload.ics_url else None
    if payload.caldav_url is not None:
        settings.caldav_url_encrypted = SENSITIVE_CONFIGURED_MARKER if payload.caldav_url else None
    if payload.username is not None:
        settings.username_encrypted = SENSITIVE_CONFIGURED_MARKER if payload.username else None
    if payload.password is not None:
        settings.password_secret_ref = SENSITIVE_CONFIGURED_MARKER if payload.password else None
    if payload.calendar_name is not None:
        settings.calendar_name = payload.calendar_name
    if payload.supports_write is not None:
        settings.supports_write = payload.supports_write

    await session.commit()
    await session.refresh(settings)
    return to_ical_settings_response(settings)


async def test_current_ical_settings(
    session: AsyncSession,
    settings_id: str,
    write: bool = False,
) -> CalendarTestResponse | None:
    result = await session.execute(select(IcalConnection).where(IcalConnection.id == settings_id))
    settings = result.scalar_one_or_none()
    if settings is None:
        return None

    await session.commit()
    if write and not settings.supports_write:
        return CalendarTestResponse(ok=False, message="CalDAV write is not configured")
    return CalendarTestResponse(ok=True, message="iCal settings exist")


def to_calendar_connection_response(
    connection: CalendarConnection,
) -> CalendarConnectionResponse:
    return CalendarConnectionResponse(
        id=connection.id,
        created_at=connection.created_at,
        updated_at=connection.updated_at,
        provider=connection.provider,
        mode=connection.mode,
        status=connection.status,
        display_name=connection.display_name,
        last_sync_at=connection.last_sync_at,
    )


def to_ical_settings_response(settings: IcalConnection) -> IcalSettingsResponse:
    return IcalSettingsResponse(
        id=settings.id,
        created_at=settings.created_at,
        updated_at=settings.updated_at,
        calendar_connection_id=settings.calendar_connection_id,
        calendar_name=settings.calendar_name,
        has_ics_url=bool(settings.ics_url_encrypted),
        has_caldav_url=bool(settings.caldav_url_encrypted),
        has_username=bool(settings.username_encrypted),
        supports_write=settings.supports_write,
    )

