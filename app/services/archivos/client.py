# app/services/archivos/client.py
from typing import List, Optional
from uuid import UUID

import httpx

from app.core.config import settings
from app.services.archivos.schemas import FileOut, PresignDownloadResponse

BASE_URL = settings.files_service_base_url.rstrip("/")
FILES_BASE = f"{BASE_URL}/v1/files"


async def upload_file(
    *,
    message_id: Optional[str],
    thread_id: Optional[str],
    file_bytes: bytes,
    filename: str,
    mime_type: str,
) -> FileOut:
    """
    Llama a POST /v1/files con multipart/form-data (campo 'upload').
    """
    params = {}
    if message_id is not None:
        params["message_id"] = message_id
    if thread_id is not None:
        params["thread_id"] = thread_id

    files = {
        "upload": (filename, file_bytes, mime_type),
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(FILES_BASE, params=params, files=files)
        resp.raise_for_status()
        return FileOut(**resp.json())


async def get_file(file_id: UUID) -> FileOut:
    url = f"{FILES_BASE}/{file_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return FileOut(**resp.json())


async def list_files(
    message_id: Optional[str] = None,
    thread_id: Optional[str] = None,
) -> List[FileOut]:
    params = {}
    if message_id is not None:
        params["message_id"] = message_id
    if thread_id is not None:
        params["thread_id"] = thread_id

    async with httpx.AsyncClient() as client:
        resp = await client.get(FILES_BASE, params=params)
        resp.raise_for_status()
        data = resp.json()
        return [FileOut(**item) for item in data]


async def delete_file(file_id: UUID) -> None:
    url = f"{FILES_BASE}/{file_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.delete(url)
        resp.raise_for_status()
        return None  # 204 No Content


async def presign_download(file_id: UUID) -> PresignDownloadResponse:
    url = f"{FILES_BASE}/{file_id}/presign-download"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url)
        resp.raise_for_status()
        return PresignDownloadResponse(**resp.json())
