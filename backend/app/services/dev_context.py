from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tenant, User, UserSettings
from app.models.enums import BookingMode, UserRole

DEV_TENANT_SLUG = "personal"
DEV_USER_EMAIL = "robin@example.local"


def default_working_hours() -> dict[str, list[dict[str, str]]]:
    return {
        "monday": [{"start": "09:00", "end": "17:00"}],
        "tuesday": [{"start": "09:00", "end": "17:00"}],
        "wednesday": [{"start": "09:00", "end": "17:00"}],
        "thursday": [{"start": "09:00", "end": "17:00"}],
        "friday": [{"start": "09:00", "end": "15:00"}],
    }


async def get_or_create_dev_user(session: AsyncSession) -> User:
    tenant = await _get_or_create_dev_tenant(session)
    result = await session.execute(select(User).where(User.email == DEV_USER_EMAIL))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            tenant_id=tenant.id,
            email=DEV_USER_EMAIL,
            display_name="Robin Gerth",
            role=UserRole.OWNER,
            timezone="Europe/Berlin",
            locale="de-DE",
        )
        session.add(user)
        await session.flush()

    await _get_or_create_user_settings(session, user)
    return user


async def _get_or_create_dev_tenant(session: AsyncSession) -> Tenant:
    result = await session.execute(select(Tenant).where(Tenant.slug == DEV_TENANT_SLUG))
    tenant = result.scalar_one_or_none()

    if tenant is not None:
        return tenant

    tenant = Tenant(name="Personal Voice Agent", slug=DEV_TENANT_SLUG, status="active")
    session.add(tenant)
    await session.flush()
    return tenant


async def _get_or_create_user_settings(session: AsyncSession, user: User) -> UserSettings:
    result = await session.execute(select(UserSettings).where(UserSettings.user_id == user.id))
    settings = result.scalar_one_or_none()

    if settings is not None:
        return settings

    settings = UserSettings(
        user_id=user.id,
        assistant_display_name="KI-Assistent von Robin Gerth",
        ai_disclosure_text="Hallo, ich bin der KI-Assistent von Robin Gerth.",
        booking_mode=BookingMode.AUTO_BOOK_CLEAR_SLOTS,
        default_appointment_duration_minutes=30,
        working_hours_json=default_working_hours(),
        buffer_before_minutes=0,
        buffer_after_minutes=15,
        store_audio_enabled=False,
        store_transcript_enabled=False,
        store_summary_enabled=True,
        whatsapp_notifications_enabled=True,
    )
    session.add(settings)
    await session.flush()
    return settings

