from typing import Optional
from uuid import UUID

import httpx
from fastapi import APIRouter, HTTPException, Header, Query, status

from app.api.mensajes.v1.schemas import (
    MessageCreateIn,
    MessageUpdateIn,
    MessageOut,
    MessagesPageOut,
)
from app.services.mensajes import client as mensajes_client

router = APIRouter(
    tags=["mensajes"],
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
    "/threads/{thread_id}/messages",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    thread_id: UUID,
    payload: MessageCreateIn,
    x_user_id: str = Header(..., alias="X-User-Id"),
):
    """
    Crea un nuevo mensaje en un hilo.

    Gateway:    POST /api/v1/mensajes/threads/{thread_id}/messages
    MS mensajes: POST /threads/{thread_id}/messages
    """
    try:
        return await mensajes_client.create_message(
            thread_id=thread_id,
            payload=payload,
            x_user_id=x_user_id,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al crear el mensaje")


@router.put(
    "/threads/{thread_id}/messages/{message_id}",
    response_model=MessageOut,
)
async def update_message(
    thread_id: UUID,
    message_id: UUID,
    payload: MessageUpdateIn,
    x_user_id: str = Header(..., alias="X-User-Id"),
):
    """
    Actualiza un mensaje de un hilo.

    Gateway:    PUT /api/v1/mensajes/threads/{thread_id}/messages/{message_id}
    MS mensajes: PUT /threads/{thread_id}/messages/{message_id}
    """
    try:
        return await mensajes_client.update_message(
            thread_id=thread_id,
            message_id=message_id,
            payload=payload,
            x_user_id=x_user_id,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al actualizar el mensaje")


@router.delete(
    "/threads/{thread_id}/messages/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_message(
    thread_id: UUID,
    message_id: UUID,
    x_user_id: str = Header(..., alias="X-User-Id"),
):
    """
    Elimina un mensaje de un hilo.

    Gateway:    DELETE /api/v1/mensajes/threads/{thread_id}/messages/{message_id}
    MS mensajes: DELETE /threads/{thread_id}/messages/{message_id}
    """
    try:
        await mensajes_client.delete_message(
            thread_id=thread_id,
            message_id=message_id,
            x_user_id=x_user_id,
        )
        # 204 No Content => FastAPI no devuelve body
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al eliminar el mensaje")


@router.get(
    "/threads/{thread_id}/messages",
    response_model=MessagesPageOut,
)
async def list_messages(
    thread_id: UUID,
    limit: int = Query(50, ge=1, le=200),
    cursor: Optional[str] = None,
):
    """
    Lista mensajes de un hilo con paginación por cursor.

    Gateway:    GET /api/v1/mensajes/threads/{thread_id}/messages?limit=&cursor=
    MS mensajes: GET /threads/{thread_id}/messages
    """
    try:
        return await mensajes_client.list_messages(
            thread_id=thread_id,
            limit=limit,
            cursor=cursor,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al listar mensajes del hilo")
