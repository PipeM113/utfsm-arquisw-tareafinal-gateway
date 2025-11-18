# app/services/mensajes/client.py
from typing import Optional
from uuid import UUID

import httpx

from app.core.config import settings
from app.services.mensajes.schemas import (
    MessageCreateIn,
    MessageUpdateIn,
    MessageOut,
    MessagesPageOut,
)

BASE_URL = settings.messages_service_base_url.rstrip("/")


async def create_message(
    thread_id: UUID,
    payload: MessageCreateIn,
    x_user_id: str,
) -> MessageOut:
    url = f"{BASE_URL}/threads/{thread_id}/messages"
    headers = {"X-User-Id": x_user_id}

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload.dict(), headers=headers)
        resp.raise_for_status()
        return MessageOut(**resp.json())


async def update_message(
    thread_id: UUID,
    message_id: UUID,
    payload: MessageUpdateIn,
    x_user_id: str,
) -> MessageOut:
    url = f"{BASE_URL}/threads/{thread_id}/messages/{message_id}"
    headers = {"X-User-Id": x_user_id}

    async with httpx.AsyncClient() as client:
        resp = await client.put(
            url,
            json=payload.dict(exclude_unset=True),
            headers=headers,
        )
        resp.raise_for_status()
        return MessageOut(**resp.json())


async def delete_message(
    thread_id: UUID,
    message_id: UUID,
    x_user_id: str,
) -> None:
    url = f"{BASE_URL}/threads/{thread_id}/messages/{message_id}"
    headers = {"X-User-Id": x_user_id}

    async with httpx.AsyncClient() as client:
        resp = await client.delete(url, headers=headers)
        resp.raise_for_status()
        # 204 No Content => no body
        return None


async def list_messages(
    thread_id: UUID,
    limit: int = 50,
    cursor: Optional[str] = None,
) -> MessagesPageOut:
    url = f"{BASE_URL}/threads/{thread_id}/messages"
    params = {"limit": limit}
    if cursor is not None:
        params["cursor"] = cursor

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return MessagesPageOut(**resp.json())
