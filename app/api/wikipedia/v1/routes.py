import httpx
from fastapi import APIRouter, HTTPException, status

from app.api.wikipedia.v1.schemas import (
    ChatWikipediaRequest,
    ChatWikipediaResponse,
)
from app.services.wikipedia import client as wikipedia_client


router = APIRouter(
    tags=["wikipedia"],
)


def _translate_httpx_error(e: httpx.HTTPError, default_message: str) -> HTTPException:
    """
    Traduce errores de httpx (del microservicio) a HTTPException para el cliente del gateway.
    """
    if isinstance(e, httpx.HTTPStatusError) and e.response is not None:
        try:
            body = e.response.json()
            detail = (
                body.get("message")
                or body.get("detail")
                or default_message
            )
        except ValueError:
            detail = default_message
        return HTTPException(
            status_code=e.response.status_code,
            detail=detail,
        )

    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=default_message,
    )


@router.post(
    "/chat",
    response_model=ChatWikipediaResponse,
    status_code=status.HTTP_200_OK,
)
async def chat_wikipedia(payload: ChatWikipediaRequest):
    """
    Endpoint del GATEWAY para preguntar al chatbot de Wikipedia.

    Gateway: POST /api/v1/wikipedia/chat
    MS:      POST /chat-wikipedia
    """
    try:
        return await wikipedia_client.chat_wikipedia(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(
            e,
            "Error al consultar el servicio de Wikipedia",
        )
