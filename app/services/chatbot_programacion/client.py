import httpx

from app.core.config import settings
from app.services.chatbot_programacion.schemas import (
    HealthResponse,
    QuestionResponse,
    ChatRequest,
    ChatResponse,
)

BASE_URL = settings.chatbot_service_base_url.rstrip("/")


async def health() -> HealthResponse:
    """
    Llama a GET /health del servicio de chatbot (quiz / wrapper).
    """
    url = f"{BASE_URL}/health"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return HealthResponse(**resp.json())


async def get_question() -> QuestionResponse:
    """
    Llama a GET /questions.
    """
    url = f"{BASE_URL}/questions"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return QuestionResponse(**resp.json())


async def publish_question() -> QuestionResponse:
    """
    Llama a POST /question/publish.
    """
    url = f"{BASE_URL}/question/publish"

    timeout = httpx.Timeout(60.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url)
        resp.raise_for_status()
        return QuestionResponse(**resp.json())


async def chat(payload: ChatRequest) -> ChatResponse:
    """
    Llama a POST /chat con el mensaje del usuario.
    """
    url = f"{BASE_URL}/chat"

    timeout = httpx.Timeout(60.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=payload.model_dump())
        resp.raise_for_status()
        return ChatResponse(**resp.json())
