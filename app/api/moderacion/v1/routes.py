from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Header, Query, status

from app.api.moderacion.v1.schemas import (
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
from app.services.moderacion import client as moderacion_client


router = APIRouter(
    tags=["moderacion"],
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


# --- ENDPOINTS PRINCIPALES ---

@router.post(
    "/check",
    response_model=ModerateMessageResponse,
)
async def moderate_message(payload: ModerateMessageRequest):
    """
    Modera un mensaje (puede aplicar strikes o bans).
    Gateway:    POST /api/v1/moderacion/check
    MS:         POST /check
    """
    try:
        return await moderacion_client.moderate_message(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al moderar el mensaje")


@router.post(
    "/analyze",
    response_model=AnalyzeTextResponse,
)
async def analyze_text(payload: AnalyzeTextRequest):
    """
    Analiza un texto sin aplicar strikes ni bans.
    Gateway:    POST /api/v1/moderacion/analyze
    MS:         POST /analyze
    """
    try:
        return await moderacion_client.analyze_text(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al analizar el texto")


@router.get(
    "/status/{user_id}/{channel_id}",
    response_model=ModerationStatusResponse,
)
async def get_status(user_id: str, channel_id: str):
    """
    Obtiene el estado de moderación de un usuario en un canal.
    Gateway:    GET /api/v1/moderacion/status/{user_id}/{channel_id}
    MS:         GET /status/{user_id}/{channel_id}
    """
    try:
        return await moderacion_client.get_status(user_id=user_id, channel_id=channel_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener estado de moderación")


# --- BLACKLIST WORDS ---

@router.post(
    "/words",
    response_model=SuccessResponse,
)
async def add_word(
    payload: AddWordRequest,
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Agrega una nueva palabra a la lista negra.
    Gateway:    POST /api/v1/moderacion/words
    MS:         POST /words
    """
    try:
        return await moderacion_client.add_word(payload=payload, api_key=api_key)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al agregar palabra a la lista negra")


@router.get(
    "/words",
    response_model=BlacklistWordsResponse,
)
async def list_words(
    language: Optional[str] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
):
    """
    Lista palabras de la lista negra con filtros opcionales.
    Gateway:    GET /api/v1/moderacion/words
    MS:         GET /words
    """
    try:
        return await moderacion_client.list_words(
            language=language,
            category=category,
            severity=severity,
            limit=limit,
            skip=skip,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al listar palabras de la lista negra")


@router.delete(
    "/words/{word_id}",
    response_model=SuccessResponse,
)
async def delete_word(
    word_id: str,
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Desactiva lógicamente una palabra de la lista negra.
    Gateway:    DELETE /api/v1/moderacion/words/{word_id}
    MS:         DELETE /words/{word_id}
    """
    try:
        return await moderacion_client.delete_word(word_id=word_id, api_key=api_key)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al eliminar palabra de la lista negra")


@router.get(
    "/stats",
    response_model=BlacklistStatsResponse,
)
async def get_blacklist_stats():
    """
    Obtiene estadísticas agregadas de la lista negra.
    Gateway:    GET /api/v1/moderacion/stats
    MS:         GET /stats
    """
    try:
        return await moderacion_client.get_blacklist_stats()
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener estadísticas de la lista negra")


@router.post(
    "/refresh-cache",
    response_model=SuccessResponse,
)
async def refresh_cache(
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Fuerza la actualización del caché de lista negra.
    Gateway:    POST /api/v1/moderacion/refresh-cache
    MS:         POST /refresh-cache
    """
    try:
        return await moderacion_client.refresh_cache(api_key=api_key)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al refrescar el caché de lista negra")


# --- BANS, VIOLACIONES Y ESTADÍSTICAS ---

@router.get(
    "/banned-users",
    response_model=BannedUsersResponse,
)
async def get_banned_users(
    api_key: str = Header(..., alias="X-API-Key"),
    channel_id: Optional[str] = None,
):
    """
    Lista usuarios baneados, opcionalmente filtrando por canal.
    Gateway:    GET /api/v1/moderacion/banned-users
    MS:         GET /banned-users
    """
    try:
        return await moderacion_client.get_banned_users(
            api_key=api_key,
            channel_id=channel_id,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener usuarios baneados")


@router.get(
    "/users/{user_id}/violations",
    response_model=UserViolationsResponse,
)
async def get_user_violations(
    user_id: str,
    channel_id: str,
    limit: int = Query(50, ge=1, le=100),
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Obtiene historial de violaciones de un usuario en un canal.
    Gateway:    GET /api/v1/moderacion/users/{user_id}/violations
    MS:         GET /users/{user_id}/violations
    """
    try:
        return await moderacion_client.get_user_violations(
            user_id=user_id,
            channel_id=channel_id,
            limit=limit,
            api_key=api_key,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener historial de violaciones")


@router.put(
    "/users/{user_id}/unban",
    response_model=SuccessResponse,
)
async def unban_user(
    user_id: str,
    payload: UnbanUserRequest,
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Desbanea a un usuario en un canal.
    Gateway:    PUT /api/v1/moderacion/users/{user_id}/unban
    MS:         PUT /users/{user_id}/unban
    """
    try:
        return await moderacion_client.unban_user(
            user_id=user_id,
            payload=payload,
            api_key=api_key,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al desbanear usuario")


@router.get(
    "/users/{user_id}/status",
    response_model=UserStatusResponse,
)
async def get_user_status(
    user_id: str,
    channel_id: str,
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Obtiene el estado completo de moderación de un usuario.
    Gateway:    GET /api/v1/moderacion/users/{user_id}/status
    MS:         GET /users/{user_id}/status
    """
    try:
        return await moderacion_client.get_user_status(
            user_id=user_id,
            channel_id=channel_id,
            api_key=api_key,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener estado del usuario")


@router.post(
    "/users/{user_id}/reset-strikes",
    response_model=SuccessResponse,
)
async def reset_strikes(
    user_id: str,
    channel_id: str,
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Resetea los strikes de un usuario en un canal.
    Gateway:    POST /api/v1/moderacion/users/{user_id}/reset-strikes
    MS:         POST /users/{user_id}/reset-strikes
    """
    try:
        return await moderacion_client.reset_strikes(
            user_id=user_id,
            channel_id=channel_id,
            api_key=api_key,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al resetear strikes del usuario")


@router.get(
    "/channels/{channel_id}/stats",
    response_model=ChannelStatsResponse,
)
async def get_channel_stats(
    channel_id: str,
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Obtiene estadísticas de moderación para un canal.
    Gateway:    GET /api/v1/moderacion/channels/{channel_id}/stats
    MS:         GET /channels/{channel_id}/stats
    """
    try:
        return await moderacion_client.get_channel_stats(
            channel_id=channel_id,
            api_key=api_key,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener estadísticas del canal")


@router.post(
    "/maintenance/expire-bans",
    response_model=SuccessResponse,
)
async def expire_bans(
    api_key: str = Header(..., alias="X-API-Key"),
):
    """
    Ejecuta tarea de mantenimiento para expirar bans temporales vencidos.
    Gateway:    POST /api/v1/moderacion/maintenance/expire-bans
    MS:         POST /maintenance/expire-bans
    """
    try:
        return await moderacion_client.expire_bans(api_key=api_key)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al expirar bans")
