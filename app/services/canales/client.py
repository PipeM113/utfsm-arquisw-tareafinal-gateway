from typing import List

import httpx

from app.core.config import settings
from app.services.canales.schemas import (
    Channel,
    ChannelBasicInfoResponse,
    ChannelCreatePayload,
    ChannelIDResponse,
    ChannelMember,
    ChannelUpdatePayload,
    ChannelUserPayload,
)

BASE_URL = settings.channels_service_base_url.rstrip("/")
CHANNELS_BASE = f"{BASE_URL}/v1/channels"
MEMBERS_BASE = f"{BASE_URL}/v1/members"


async def create_channel(payload: ChannelCreatePayload) -> Channel:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{CHANNELS_BASE}/", json=payload.dict())
        resp.raise_for_status()
        return Channel(**resp.json())


async def list_channels(page: int = 1, page_size: int = 10) -> List[ChannelBasicInfoResponse]:
    params = {"page": page, "page_size": page_size}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CHANNELS_BASE}/", params=params)
        resp.raise_for_status()
        data = resp.json()
        return [ChannelBasicInfoResponse(**item) for item in data]


async def get_channel(channel_id: str) -> Channel:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CHANNELS_BASE}/{channel_id}")
        resp.raise_for_status()
        return Channel(**resp.json())


async def update_channel(channel_id: str, payload: ChannelUpdatePayload) -> Channel:
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"{CHANNELS_BASE}/{channel_id}",
            json=payload.dict(exclude_unset=True),
        )
        resp.raise_for_status()
        return Channel(**resp.json())


async def deactivate_channel(channel_id: str) -> ChannelIDResponse:
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{CHANNELS_BASE}/{channel_id}")
        resp.raise_for_status()
        return ChannelIDResponse(**resp.json())


async def reactivate_channel(channel_id: str) -> ChannelIDResponse:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{CHANNELS_BASE}/{channel_id}/reactivate")
        resp.raise_for_status()
        return ChannelIDResponse(**resp.json())


async def get_channel_basic_info(channel_id: str) -> ChannelBasicInfoResponse:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CHANNELS_BASE}/{channel_id}/basic")
        resp.raise_for_status()
        return ChannelBasicInfoResponse(**resp.json())


async def add_member(payload: ChannelUserPayload) -> Channel:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{MEMBERS_BASE}/", json=payload.dict())
        resp.raise_for_status()
        return Channel(**resp.json())


async def remove_member(payload: ChannelUserPayload) -> Channel:
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method="DELETE",
            url=f"{MEMBERS_BASE}/",
            json=payload.dict()
        )
        resp.raise_for_status()
        return Channel(**resp.json())


async def get_channels_for_user(user_id: str) -> List[ChannelBasicInfoResponse]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{MEMBERS_BASE}/{user_id}")
        resp.raise_for_status()
        data = resp.json()
        return [ChannelBasicInfoResponse(**item) for item in data]


async def get_channels_for_owner(owner_id: str) -> List[ChannelBasicInfoResponse]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{MEMBERS_BASE}/owner/{owner_id}")
        resp.raise_for_status()
        data = resp.json()
        return [ChannelBasicInfoResponse(**item) for item in data]


async def get_members_for_channel(
    channel_id: str,
    page: int = 1,
    page_size: int = 100,
) -> List[ChannelMember]:
    params = {"page": page, "page_size": page_size}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{MEMBERS_BASE}/channel/{channel_id}", params=params)
        resp.raise_for_status()
        data = resp.json()
        return [ChannelMember(**item) for item in data]
