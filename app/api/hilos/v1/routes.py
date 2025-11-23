# app/api/hilos/v1/routes.py
from typing import List, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query, status

from app.api.hilos.v1.schemas import (
    ThreadCreate,
    ThreadUpdate,
    ThreadOut,
    ThreadBasicInfo
)
from app.services.hilos import client as hilos_client


router = APIRouter(
    tags=["hilos"],
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
    "/",
    response_model=ThreadOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_thread(payload: ThreadCreate):
    """
    Crea un nuevo hilo en un canal existente.

    Gateway: POST /api/v1/hilos/
    MS hilos: POST /v1/
    """
    try:
        return await hilos_client.create_thread(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al crear el hilo")


@router.get(
    "/",
    response_model=List[ThreadBasicInfo],
)
async def list_threads(
    channel_id: Optional[str] = Query(
        None,
        description="Filtrar por ID de canal (opcional)",
    ),
):
    """
    Lista todos los hilos no eliminados, opcionalmente filtrando por canal.

    Gateway: GET /api/v1/hilos/?channel_id=
    MS hilos: GET /v1/
    """
    try:
        return await hilos_client.get_threads_by_channel(channel_id=channel_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al listar hilos")


@router.get(
    "/{thread_id}",
    response_model=ThreadOut,
)
async def get_thread(thread_id: str):
    """
    Obtiene la información detallada de un hilo por su identificador.

    Gateway: GET /api/v1/hilos/{thread_id}
    MS hilos: GET /v1/{thread_id}
    """
    try:
        return await hilos_client.get_thread(thread_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener el hilo")


@router.patch(
    "/{thread_id}",
    response_model=ThreadOut,
)
async def update_thread(
    thread_id: str,
    payload: ThreadUpdate,
):
    """
    Actualiza parcialmente un hilo (título, estado y/o metadata).

    Gateway: PATCH /api/v1/hilos/{thread_id}
    MS hilos: PATCH /v1/{thread_id}
    """
    try:
        return await hilos_client.update_thread(thread_id=thread_id, payload=payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al actualizar el hilo")


@router.post(
    "/{thread_id}/archive",
    response_model=ThreadOut,
)
async def archive_thread(thread_id: str):
    """
    Archiva un hilo, cambiando su estado a 'archived'.

    Gateway: POST /api/v1/hilos/{thread_id}/archive
    MS hilos: POST /v1/{thread_id}:archive
    """
    try:
        return await hilos_client.archive_thread(thread_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al archivar el hilo")


@router.delete(
    "/{thread_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_thread(thread_id: str):
    """
    Marca un hilo como eliminado lógicamente.

    Gateway: DELETE /api/v1/hilos/{thread_id}
    MS hilos: DELETE /v1/{thread_id}
    """
    try:
        await hilos_client.delete_thread(thread_id)
        # 204 No Content -> sin body
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al eliminar el hilo")
