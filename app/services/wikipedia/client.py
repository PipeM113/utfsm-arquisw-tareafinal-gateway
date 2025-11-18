# app/services/wikipedia/client.py
import httpx

from app.core.config import settings
from app.services.wikipedia.schemas import (
    ChatWikipediaRequest,
    ChatWikipediaResponse,
)

BASE_URL = settings.wikipedia_service_base_url.rstrip("/")


async def chat_wikipedia(payload: ChatWikipediaRequest) -> ChatWikipediaResponse:
    """
    Llama al endpoint /chat-wikipedia del servicio de Wikipedia.
    """
    url = f"{BASE_URL}/chat-wikipedia"

    timeout = httpx.Timeout(
        60.0,
        connect=10.0,
        read=60.0,
        write=10.0,
        pool=None,
    )

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=payload.model_dump())
        resp.raise_for_status()
        return ChatWikipediaResponse(**resp.json())
