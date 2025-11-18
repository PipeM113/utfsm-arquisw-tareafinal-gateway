# app/api/canales/v1/routes.py
from typing import List

import httpx
from fastapi import APIRouter, HTTPException, status

from app.api.canales.v1.schemas import (
    Channel,
    ChannelBasicInfoResponse,
    ChannelCreatePayload,
    ChannelIDResponse,
    ChannelMember,
    ChannelUpdatePayload,
    ChannelUserPayload,
)
from app.services.canales import client as canales_client

router = APIRouter(
    tags=["canales"],
)


def _translate_httpx_error(e: httpx.HTTPError, default_message: str) -> HTTPException:
    """
    Traduce errores de httpx (llamadas al MS) a HTTPException hacia el cliente del gateway.
    """
    if isinstance(e, httpx.HTTPStatusError) and e.response is not None:
        try:
            body = e.response.json()
            detail = body.get("detail", default_message)
        except ValueError:
            detail = default_message
        return HTTPException(
            status_code=e.response.status_code,
            detail=detail,
        )

    # Errores de red, timeouts, etc.
    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=default_message,
    )


@router.post(
    "/",
    response_model=Channel,
    status_code=status.HTTP_201_CREATED,
)
async def create_channel(payload: ChannelCreatePayload):
    """
    Crea un nuevo canal a través del gateway.

    Gateway:   POST /api/v1/canales/
    MS canales: POST /v1/channels/
    """
    try:
        return await canales_client.create_channel(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al crear el canal")


@router.get(
    "/",
    response_model=List[ChannelBasicInfoResponse],
)
async def list_channels(page: int = 1, page_size: int = 10):
    """
    Lista canales (paginado).

    Gateway:   GET /api/v1/canales/?page=&page_size=
    MS canales: GET /v1/channels/
    """
    try:
        return await canales_client.list_channels(page=page, page_size=page_size)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al listar canales")


@router.get(
    "/{channel_id}",
    response_model=Channel,
)
async def get_channel(channel_id: str):
    """
    Obtiene un canal por ID.

    Gateway:   GET /api/v1/canales/{channel_id}
    MS canales: GET /v1/channels/{channel_id}
    """
    try:
        return await canales_client.get_channel(channel_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener el canal")


@router.put(
    "/{channel_id}",
    response_model=Channel,
)
async def update_channel(channel_id: str, payload: ChannelUpdatePayload):
    """
    Actualiza un canal.

    Gateway:   PUT /api/v1/canales/{channel_id}
    MS canales: PUT /v1/channels/{channel_id}
    """
    try:
        return await canales_client.update_channel(channel_id, payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al actualizar el canal")


@router.delete(
    "/{channel_id}",
    response_model=ChannelIDResponse,
)
async def deactivate_channel(channel_id: str):
    """
    Desactiva lógicamente un canal.

    Gateway:   DELETE /api/v1/canales/{channel_id}
    MS canales: DELETE /v1/channels/{channel_id}
    """
    try:
        return await canales_client.deactivate_channel(channel_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al desactivar el canal")


@router.post(
    "/{channel_id}/reactivate",
    response_model=ChannelIDResponse,
)
async def reactivate_channel(channel_id: str):
    """
    Reactiva un canal desactivado.

    Gateway:   POST /api/v1/canales/{channel_id}/reactivate
    MS canales: POST /v1/channels/{channel_id}/reactivate
    """
    try:
        return await canales_client.reactivate_channel(channel_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al reactivar el canal")


@router.get(
    "/{channel_id}/basic",
    response_model=ChannelBasicInfoResponse,
)
async def get_channel_basic_info(channel_id: str):
    """
    Obtiene info básica de un canal.

    Gateway:   GET /api/v1/canales/{channel_id}/basic
    MS canales: GET /v1/channels/{channel_id}/basic
    """
    try:
        return await canales_client.get_channel_basic_info(channel_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener información básica del canal")


# --- Rutas relacionadas a miembros ---


@router.post(
    "/members/",
    response_model=Channel,
)
async def add_member(payload: ChannelUserPayload):
    """
    Agrega un usuario a un canal.

    Gateway:   POST /api/v1/canales/members/
    MS canales: POST /v1/members/
    """
    try:
        return await canales_client.add_member(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al agregar miembro al canal")


@router.delete(
    "/members/",
    response_model=Channel,
)
async def remove_member(payload: ChannelUserPayload):
    """
    Elimina un usuario de un canal.

    Gateway:   DELETE /api/v1/canales/members/
    MS canales: DELETE /v1/members/
    """
    try:
        return await canales_client.remove_member(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al eliminar miembro del canal")


@router.get(
    "/members/{user_id}",
    response_model=List[ChannelBasicInfoResponse],
)
async def get_channels_for_user(user_id: str):
    """
    Obtiene todos los canales en los que un usuario es miembro.

    Gateway:   GET /api/v1/canales/members/{user_id}
    MS canales: GET /v1/members/{user_id}
    """
    try:
        return await canales_client.get_channels_for_user(user_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener canales del usuario")


@router.get(
    "/members/owner/{owner_id}",
    response_model=List[ChannelBasicInfoResponse],
)
async def get_channels_for_owner(owner_id: str):
    """
    Obtiene todos los canales asociados a un propietario.

    Gateway:   GET /api/v1/canales/members/owner/{owner_id}
    MS canales: GET /v1/members/owner/{owner_id}
    """
    try:
        return await canales_client.get_channels_for_owner(owner_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener canales del propietario")


@router.get(
    "/members/channel/{channel_id}",
    response_model=List[ChannelMember],
)
async def get_members_for_channel(
    channel_id: str,
    page: int = 1,
    page_size: int = 100,
):
    """
    Obtiene los miembros de un canal (paginado).

    Gateway:   GET /api/v1/canales/members/channel/{channel_id}?page=&page_size=
    MS canales: GET /v1/members/channel/{channel_id}
    """
    try:
        return await canales_client.get_members_for_channel(
            channel_id=channel_id,
            page=page,
            page_size=page_size,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener miembros del canal")
