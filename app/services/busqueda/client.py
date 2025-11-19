from datetime import datetime
from typing import List, Optional

import httpx

from app.core.config import settings
from app.services.busqueda.schemas import IndexEnum, SearchResponse

BASE_URL = settings.search_service_base_url.rstrip("/")


# --- BÚSQUEDA GENERAL (sobre mensajes, hilos, archivos, canales) ---

async def general_search(
    q: Optional[str] = None,
    channel_id: Optional[int] = None,
    thread_id: Optional[int] = None,
    author_id: Optional[int] = None,
    index: Optional[List[IndexEnum]] = None,
    limit: int = 10,
    offset: int = 0,
) -> SearchResponse:
    """
    GET /

    Realiza una búsqueda general en Elasticsearch sobre mensajes, hilos,
    archivos y canales, con filtros opcionales.
    """
    url = f"{BASE_URL}/"
    params: dict = {
        "limit": limit,
        "offset": offset,
    }
    if q is not None:
        params["q"] = q
    if channel_id is not None:
        params["channel_id"] = channel_id
    if thread_id is not None:
        params["thread_id"] = thread_id
    if author_id is not None:
        params["author_id"] = author_id
    if index:
        # lista de enums -> lista de strings
        params["index"] = [i.value for i in index]

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return SearchResponse(**resp.json())


# --- BÚSQUEDAS SOBRE HILOS ---

async def search_thread_by_id(thread_id: str) -> SearchResponse:
    """
    GET /threads/id/{thread_id}
    """
    url = f"{BASE_URL}/threads/id/{thread_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return SearchResponse(**resp.json())


async def search_threads_by_category(thread_category: str) -> SearchResponse:
    """
    GET /threads/category/{thread_category}
    """
    url = f"{BASE_URL}/threads/category/{thread_category}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return SearchResponse(**resp.json())


async def search_threads_by_author(thread_author: str) -> SearchResponse:
    """
    GET /threads/author/{thread_author}
    """
    url = f"{BASE_URL}/threads/author/{thread_author}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return SearchResponse(**resp.json())


async def search_threads_by_date_range(
    start_date: datetime,
    end_date: datetime,
) -> SearchResponse:
    """
    GET /threads/daterange?start_date=&end_date=
    """
    url = f"{BASE_URL}/threads/daterange"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return SearchResponse(**resp.json())


async def search_threads_by_tag(thread_tag: str) -> SearchResponse:
    """
    GET /threads/tag/{thread_tag}
    """
    url = f"{BASE_URL}/threads/tag/{thread_tag}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return SearchResponse(**resp.json())


async def search_threads_by_keyword(thread_keyword: str) -> SearchResponse:
    """
    GET /threads/keyword/{thread_keyword}
    """
    url = f"{BASE_URL}/threads/keyword/{thread_keyword}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return SearchResponse(**resp.json())


# --- BÚSQUEDA DE MENSAJES ---

async def search_messages(
    q: Optional[str] = None,
    author_id: Optional[int] = None,
    thread_id: Optional[int] = None,
    message_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
) -> SearchResponse:
    """
    GET /message/search_message
    """
    url = f"{BASE_URL}/message/search_message"
    params: dict = {
        "limit": limit,
        "offset": offset,
    }
    if q is not None:
        params["q"] = q
    if author_id is not None:
        params["author_id"] = author_id
    if thread_id is not None:
        params["thread_id"] = thread_id
    if message_id is not None:
        params["message_id"] = message_id

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return SearchResponse(**resp.json())


# --- BÚSQUEDA DE ARCHIVOS ---

async def search_files(
    q: Optional[str] = None,
    thread_id: Optional[int] = None,
    message_id: Optional[int] = None,
    pages_min: Optional[int] = None,
    pages_max: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
) -> SearchResponse:
    """
    GET /files/search_files
    """
    url = f"{BASE_URL}/files/search_files"
    params: dict = {
        "limit": limit,
        "offset": offset,
    }
    if q is not None:
        params["q"] = q
    if thread_id is not None:
        params["thread_id"] = thread_id
    if message_id is not None:
        params["message_id"] = message_id
    if pages_min is not None:
        params["pages_min"] = pages_min
    if pages_max is not None:
        params["pages_max"] = pages_max

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return SearchResponse(**resp.json())
