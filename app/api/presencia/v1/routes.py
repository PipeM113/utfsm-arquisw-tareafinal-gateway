from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Query, status

from app.api.presencia.v1.schemas import (
    DeviceEnum,
    StatusEnum,
    UserConnection,
    HealthResponse,
    PresenceCreateResponse,
    PresenceListResponse,
    PresenceStatsResponse,
    SinglePresenceResponse,
    StatusUpdateRequest,
    SimpleResponse,
)
from app.services.presencia import client as presencia_client


router = APIRouter(
    tags=["presencia"],
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


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health_check():
    """
    Verifica que el servicio de presencia esté operativo.
    Gateway:    GET /api/v1/presencia/health
    MS:         GET /api/v1.0.0/presence/health
    """
    try:
        return await presencia_client.health()
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al verificar salud del servicio de presencia")


@router.post(
    "/",
    response_model=PresenceCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def connect_user(payload: UserConnection):
    """
    Registra la conexión de un usuario y lo marca como online.

    Gateway:    POST /api/v1/presencia/
    MS:         POST /api/v1.0.0/presence
    """
    try:
        return await presencia_client.connect_user(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al registrar la presencia del usuario")


@router.get(
    "/",
    response_model=PresenceListResponse,
)
async def list_presence(
    status: Optional[StatusEnum] = Query(None, description="online u offline"),
):
    """
    Lista usuarios con su estado de presencia actual, opcionalmente filtrando por estado.

    Gateway:    GET /api/v1/presencia/?status=
    MS:         GET /api/v1.0.0/presence
    """
    try:
        return await presencia_client.list_presence(status=status)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al listar presencia de usuarios")


@router.get(
    "/stats",
    response_model=PresenceStatsResponse,
)
async def get_stats():
    """
    Devuelve estadísticas agregadas de presencia.

    Gateway:    GET /api/v1/presencia/stats
    MS:         GET /api/v1.0.0/presence/stats
    """
    try:
        return await presencia_client.get_stats()
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener estadísticas de presencia")


@router.get(
    "/{user_id}",
    response_model=SinglePresenceResponse,
)
async def get_user_presence(user_id: str):
    """
    Obtiene la información de presencia de un usuario específico.

    Gateway:    GET /api/v1/presencia/{user_id}
    MS:         GET /api/v1.0.0/presence/{userId}
    """
    try:
        return await presencia_client.get_user_presence(user_id=user_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener presencia del usuario")


@router.patch(
    "/{user_id}",
    response_model=SimpleResponse,
)
async def update_user_presence(
    user_id: str,
    payload: StatusUpdateRequest,
):
    """
    Actualiza el estado de un usuario (online/offline) o envía un heartbeat.

    Gateway:    PATCH /api/v1/presencia/{user_id}
    MS:         PATCH /api/v1.0.0/presence/{userId}
    """
    try:
        return await presencia_client.update_user_presence(
            user_id=user_id,
            payload=payload,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al actualizar la presencia del usuario")


@router.delete(
    "/{user_id}",
    response_model=SimpleResponse,
)
async def delete_user_presence(user_id: str):
    """
    Elimina completamente la información de presencia de un usuario.

    Gateway:    DELETE /api/v1/presencia/{user_id}
    MS:         DELETE /api/v1.0.0/presence/{userId}
    """
    try:
        return await presencia_client.delete_user_presence(user_id=user_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al eliminar presencia del usuario")
