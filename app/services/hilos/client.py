# app/services/hilos/client.py
from typing import List, Optional

import httpx

from app.core.config import settings
from app.services.hilos.schemas import ThreadCreate, ThreadOut, ThreadUpdate, ThreadBasicInfo

BASE_URL = settings.threads_service_base_url.rstrip("/")
BASE_URL = f"{BASE_URL}/threads"
THREADS_BASE = f"{BASE_URL}/threads"
CHANNELS_BASE = f"{BASE_URL}/channel"


async def create_thread(payload: ThreadCreate) -> ThreadOut:
    """
    POST /v1/  -> crea un nuevo hilo y devuelve ThreadOut.
    """
    url = f"{THREADS_BASE}/?channel_id={payload.channel_id}&thread_name={payload.title}&user_id={payload.created_by}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload.dict())
        resp.raise_for_status()
        return ThreadOut(**resp.json())


async def list_threads(channel_id: Optional[str] = None) -> List[ThreadOut]:
    """
    GET /v1/  -> lista hilos, opcionalmente filtrando por channel_id.
    """
    url = f"{THREADS_BASE}/"
    params = {}
    if channel_id is not None:
        params["channel_id"] = channel_id

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return [ThreadOut(**item) for item in data]


async def get_thread(thread_id: str) -> ThreadOut:
    """
    GET /v1/{thread_id}
    """
    url = f"{THREADS_BASE}/{thread_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return ThreadOut(**resp.json())


async def update_thread(thread_id: str, payload: ThreadUpdate) -> ThreadOut:
    """
    PATCH /v1/{thread_id}
    """
    url = f"{THREADS_BASE}/{thread_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.patch(
            url,
            json=payload.dict(exclude_unset=True),
        )
        resp.raise_for_status()
        return ThreadOut(**resp.json())


async def archive_thread(thread_id: str) -> ThreadOut:
    """
    POST /v1/{thread_id}:archive
    """
    url = f"{THREADS_BASE}/{thread_id}:archive"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url)
        resp.raise_for_status()
        return ThreadOut(**resp.json())


async def delete_thread(thread_id: str) -> None:
    """
    DELETE /v1/{thread_id}  -> 204 No Content
    """
    url = f"{THREADS_BASE}/{thread_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.delete(url)
        resp.raise_for_status()
        return None


async def get_threads_by_channel(channel_id: str) -> List[ThreadBasicInfo]:
    """
    GET /v1/channel/{channel_id}/threads  -> lista hilos de un canal específico.
    """
    url = f"{CHANNELS_BASE}/get_threads?channel_id={channel_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return [ThreadBasicInfo(**item) for item in data]