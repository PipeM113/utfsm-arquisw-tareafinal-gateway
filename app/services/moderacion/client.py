from typing import Optional

import httpx

from app.core.config import settings
from app.services.moderacion.schemas import (
    ModerateMessageRequest,
    ModerateMessageResponse,
    AnalyzeTextRequest,
    AnalyzeTextResponse,
    ModerationStatusResponse,
    AddWordRequest,
    SuccessResponse,
    BlacklistWordsResponse,
    BlacklistStatsResponse,
    BannedUsersResponse,
    UserViolationsResponse,
    UnbanUserRequest,
    UserStatusResponse,
    ChannelStatsResponse,
)

BASE_URL = settings.moderation_service_base_url.rstrip("/")
MODERATION_BASE = f"{BASE_URL}/api/v1/moderation"
BLACKLIST_BASE = f"{BASE_URL}/api/v1/blacklist"
ADMIN_BASE = f"{BASE_URL}/api/v1/admin"


def _api_key_header(api_key: Optional[str]) -> dict:
    # Suponemos uso de header estándar X-API-Key
    return {"X-API-Key": api_key} if api_key else {}


# --- ENDPOINTS PRINCIPALES ---

async def moderate_message(
    payload: ModerateMessageRequest,
) -> ModerateMessageResponse:
    url = f"{MODERATION_BASE}/check"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload.dict())
        resp.raise_for_status()
        return ModerateMessageResponse(**resp.json())


async def analyze_text(
    payload: AnalyzeTextRequest,
) -> AnalyzeTextResponse:
    url = f"{MODERATION_BASE}/analyze"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload.dict())
        resp.raise_for_status()
        return AnalyzeTextResponse(**resp.json())


async def get_status(
    user_id: str,
    channel_id: str,
) -> ModerationStatusResponse:
    url = f"{MODERATION_BASE}/status/{user_id}/{channel_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return ModerationStatusResponse(**resp.json())


# --- PALABRAS (BLACKLIST) ---

async def add_word(
    payload: AddWordRequest,
    api_key: str,
) -> SuccessResponse:
    url = f"{BLACKLIST_BASE}/words"
    headers = _api_key_header(api_key)
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload.dict(), headers=headers)
        resp.raise_for_status()
        return SuccessResponse(**resp.json())


async def list_words(
    language: Optional[str] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    skip: int = 0,
) -> BlacklistWordsResponse:
    url = f"{BLACKLIST_BASE}/words"
    params = {
        "limit": limit,
        "skip": skip,
    }
    if language is not None:
        params["language"] = language
    if category is not None:
        params["category"] = category
    if severity is not None:
        params["severity"] = severity

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return BlacklistWordsResponse(**resp.json())


async def delete_word(
    word_id: str,
    api_key: str,
) -> SuccessResponse:
    url = f"{BLACKLIST_BASE}/words/{word_id}"
    headers = _api_key_header(api_key)
    async with httpx.AsyncClient() as client:
        resp = await client.delete(url, headers=headers)
        resp.raise_for_status()
        return SuccessResponse(**resp.json())


async def get_blacklist_stats() -> BlacklistStatsResponse:
    url = f"{BLACKLIST_BASE}/stats"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return BlacklistStatsResponse(**resp.json())


async def refresh_cache(api_key: str) -> SuccessResponse:
    url = f"{BLACKLIST_BASE}/refresh-cache"
    headers = _api_key_header(api_key)
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers)
        resp.raise_for_status()
        return SuccessResponse(**resp.json())


# --- BANS Y VIOLACIONES ---

async def get_banned_users(
    api_key: str,
    channel_id: Optional[str] = None,
) -> BannedUsersResponse:
    url = f"{ADMIN_BASE}/banned-users"
    headers = _api_key_header(api_key)
    params = {}
    if channel_id is not None:
        params["channel_id"] = channel_id

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return BannedUsersResponse(**resp.json())


async def get_user_violations(
    user_id: str,
    channel_id: str,
    limit: int = 50,
    api_key: str = "",
) -> UserViolationsResponse:
    url = f"{ADMIN_BASE}/users/{user_id}/violations"
    headers = _api_key_header(api_key)
    params = {"channel_id": channel_id, "limit": limit}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return UserViolationsResponse(**resp.json())


async def unban_user(
    user_id: str,
    payload: UnbanUserRequest,
    api_key: str,
) -> SuccessResponse:
    url = f"{ADMIN_BASE}/users/{user_id}/unban"
    headers = _api_key_header(api_key)

    async with httpx.AsyncClient() as client:
        resp = await client.put(url, headers=headers, json=payload.dict())
        resp.raise_for_status()
        return SuccessResponse(**resp.json())


async def get_user_status(
    user_id: str,
    channel_id: str,
    api_key: str,
) -> UserStatusResponse:
    url = f"{ADMIN_BASE}/users/{user_id}/status"
    headers = _api_key_header(api_key)
    params = {"channel_id": channel_id}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return UserStatusResponse(**resp.json())


async def reset_strikes(
    user_id: str,
    channel_id: str,
    api_key: str,
) -> SuccessResponse:
    url = f"{ADMIN_BASE}/users/{user_id}/reset-strikes"
    headers = _api_key_header(api_key)
    params = {"channel_id": channel_id}

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, params=params)
        resp.raise_for_status()
        return SuccessResponse(**resp.json())


async def get_channel_stats(
    channel_id: str,
    api_key: str,
) -> ChannelStatsResponse:
    url = f"{ADMIN_BASE}/channels/{channel_id}/stats"
    headers = _api_key_header(api_key)

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return ChannelStatsResponse(**resp.json())


async def expire_bans(api_key: str) -> SuccessResponse:
    url = f"{ADMIN_BASE}/maintenance/expire-bans"
    headers = _api_key_header(api_key)

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers)
        resp.raise_for_status()
        return SuccessResponse(**resp.json())
