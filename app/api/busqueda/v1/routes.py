from datetime import datetime
from typing import List, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.api.busqueda.v1.schemas import (
    IndexEnum,
    SearchResponse,
)
from app.services.busqueda import client as busqueda_client


router = APIRouter(
    tags=["busqueda"],
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
        status_code=502,
        detail=default_message,
    )


# --- BÚSQUEDA GENERAL ---

@router.get(
    "/",
    response_model=SearchResponse,
)
async def general_search(
    q: Optional[str] = None,
    channel_id: Optional[int] = None,
    thread_id: Optional[int] = None,
    author_id: Optional[int] = None,
    index: Optional[List[IndexEnum]] = Query(
        None,
        description='Índices a consultar: "all", "messages", "threads", "files"',
    ),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Búsqueda general sobre mensajes, hilos, archivos y canales.

    Gateway: GET /api/v1/busqueda/
    MS:      GET /
    """
    try:
        return await busqueda_client.general_search(
            q=q,
            channel_id=channel_id,
            thread_id=thread_id,
            author_id=author_id,
            index=index,
            limit=limit,
            offset=offset,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error en la búsqueda general")


# --- HILOS (threads) ---

@router.get(
    "/threads/id/{thread_id}",
    response_model=SearchResponse,
)
async def search_thread_by_id(thread_id: str):
    """
    Gateway: GET /api/v1/busqueda/threads/id/{thread_id}
    MS:      GET /threads/id/{thread_id}
    """
    try:
        return await busqueda_client.search_thread_by_id(thread_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al buscar hilo por ID")


@router.get(
    "/threads/category/{thread_category}",
    response_model=SearchResponse,
)
async def search_threads_by_category(thread_category: str):
    """
    Gateway: GET /api/v1/busqueda/threads/category/{thread_category}
    MS:      GET /threads/category/{thread_category}
    """
    try:
        return await busqueda_client.search_threads_by_category(thread_category)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al buscar hilos por categoría")


@router.get(
    "/threads/author/{thread_author}",
    response_model=SearchResponse,
)
async def search_threads_by_author(thread_author: str):
    """
    Gateway: GET /api/v1/busqueda/threads/author/{thread_author}
    MS:      GET /threads/author/{thread_author}
    """
    try:
        return await busqueda_client.search_threads_by_author(thread_author)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al buscar hilos por autor")


@router.get(
    "/threads/daterange",
    response_model=SearchResponse,
)
async def search_threads_by_date_range(
    start_date: datetime,
    end_date: datetime,
):
    """
    Gateway: GET /api/v1/busqueda/threads/daterange?start_date=&end_date=
    MS:      GET /threads/daterange
    """
    try:
        return await busqueda_client.search_threads_by_date_range(
            start_date=start_date,
            end_date=end_date,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al buscar hilos por rango de fecha")


@router.get(
    "/threads/tag/{thread_tag}",
    response_model=SearchResponse,
)
async def search_threads_by_tag(thread_tag: str):
    """
    Gateway: GET /api/v1/busqueda/threads/tag/{thread_tag}
    MS:      GET /threads/tag/{thread_tag}
    """
    try:
        return await busqueda_client.search_threads_by_tag(thread_tag)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al buscar hilos por tag")


@router.get(
    "/threads/keyword/{thread_keyword}",
    response_model=SearchResponse,
)
async def search_threads_by_keyword(thread_keyword: str):
    """
    Gateway: GET /api/v1/busqueda/threads/keyword/{thread_keyword}
    MS:      GET /threads/keyword/{thread_keyword}
    """
    try:
        return await busqueda_client.search_threads_by_keyword(thread_keyword)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al buscar hilos por keyword")


# --- MENSAJES (message) ---

@router.get(
    "/message/search_message",
    response_model=SearchResponse,
)
async def search_messages(
    q: Optional[str] = None,
    author_id: Optional[int] = None,
    thread_id: Optional[int] = None,
    message_id: Optional[int] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Gateway: GET /api/v1/busqueda/message/search_message
    MS:      GET /message/search_message
    """
    try:
        return await busqueda_client.search_messages(
            q=q,
            author_id=author_id,
            thread_id=thread_id,
            message_id=message_id,
            limit=limit,
            offset=offset,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al buscar mensajes")


# --- ARCHIVOS (files) ---

@router.get(
    "/files/search_files",
    response_model=SearchResponse,
)
async def search_files(
    q: Optional[str] = None,
    thread_id: Optional[int] = None,
    message_id: Optional[int] = None,
    pages_min: Optional[int] = None,
    pages_max: Optional[int] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Gateway: GET /api/v1/busqueda/files/search_files
    MS:      GET /files/search_files
    """
    try:
        return await busqueda_client.search_files(
            q=q,
            thread_id=thread_id,
            message_id=message_id,
            pages_min=pages_min,
            pages_max=pages_max,
            limit=limit,
            offset=offset,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al buscar archivos")
