from typing import Optional

import httpx

from app.core.config import settings
from app.services.presencia.schemas import (
    HealthResponse,
    PresenceCreateResponse,
    PresenceListResponse,
    PresenceStatsResponse,
    SinglePresenceResponse,
    StatusUpdateRequest,
    SimpleResponse,
    StatusEnum,
    UserConnection,
)

BASE_URL = settings.presence_service_base_url.rstrip("/")
PRESENCE_BASE = f"{BASE_URL}/api/v1.0.0/presence"


async def health() -> HealthResponse:
    url = f"{PRESENCE_BASE}/health"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return HealthResponse(**resp.json())


async def connect_user(payload: UserConnection) -> PresenceCreateResponse:
    url = PRESENCE_BASE
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload.dict())
        resp.raise_for_status()
        return PresenceCreateResponse(**resp.json())


async def list_presence(
    status: Optional[StatusEnum] = None,
) -> PresenceListResponse:
    url = PRESENCE_BASE
    params = {}
    if status is not None:
        params["status"] = status.value

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return PresenceListResponse(**resp.json())


async def get_stats() -> PresenceStatsResponse:
    url = f"{PRESENCE_BASE}/stats"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return PresenceStatsResponse(**resp.json())


async def get_user_presence(user_id: str) -> SinglePresenceResponse:
    url = f"{PRESENCE_BASE}/{user_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return SinglePresenceResponse(**resp.json())


async def update_user_presence(
    user_id: str,
    payload: StatusUpdateRequest,
) -> SimpleResponse:
    url = f"{PRESENCE_BASE}/{user_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.patch(url, json=payload.dict(exclude_unset=True))
        resp.raise_for_status()
        return SimpleResponse(**resp.json())


async def delete_user_presence(user_id: str) -> SimpleResponse:
    url = f"{PRESENCE_BASE}/{user_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.delete(url)
        resp.raise_for_status()
        return SimpleResponse(**resp.json())
