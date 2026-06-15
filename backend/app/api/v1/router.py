from fastapi import APIRouter

from app.api.v1.routes import (
    appointments,
    calendar_connections,
    calls,
    health,
    ical_settings,
    provider_settings,
    user_settings,
    webhooks,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(user_settings.router, tags=["user-settings"])
api_router.include_router(calls.router, tags=["calls"])
api_router.include_router(appointments.router, tags=["appointments"])
api_router.include_router(calendar_connections.router, tags=["calendar-connections"])
api_router.include_router(ical_settings.router, tags=["ical-settings"])
api_router.include_router(provider_settings.router, tags=["provider-settings"])
api_router.include_router(webhooks.router, tags=["webhooks"])
