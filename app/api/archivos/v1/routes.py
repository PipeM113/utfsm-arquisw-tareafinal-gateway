# app/api/archivos/v1/routes.py
from typing import List, Optional
from uuid import UUID

import httpx
from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    UploadFile,
    File,
    status,
)

from app.api.archivos.v1.schemas import (
    FileOut,
    PresignDownloadResponse,
)
from app.services.archivos import client as archivos_client


router = APIRouter(
    tags=["archivos"],
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
    response_model=FileOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    message_id: Optional[str] = Query(
        None,
        description="ID del mensaje asociado (opcional, pero debe ir message_id o thread_id)",
    ),
    thread_id: Optional[str] = Query(
        None,
        description="ID del hilo asociado (opcional, pero debe ir message_id o thread_id)",
    ),
    upload: UploadFile = File(..., description="Archivo a subir"),
):
    """
    Sube un archivo y lo asocia a un mensaje o hilo.

    Gateway:    POST /api/v1/archivos/
    MS archivos: POST /v1/files
    """
    if message_id is None and thread_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar message_id o thread_id",
        )

    try:
        file_bytes = await upload.read()
        return await archivos_client.upload_file(
            message_id=message_id,
            thread_id=thread_id,
            file_bytes=file_bytes,
            filename=upload.filename or "upload",
            mime_type=upload.content_type or "application/octet-stream",
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al subir el archivo")


@router.get(
    "/{file_id}",
    response_model=FileOut,
)
async def get_file(file_id: UUID):
    """
    Obtiene la metadata de un archivo por ID.

    Gateway:    GET /api/v1/archivos/{file_id}
    MS archivos: GET /v1/files/{file_id}
    """
    try:
        return await archivos_client.get_file(file_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener información del archivo")


@router.get(
    "/",
    response_model=List[FileOut],
)
async def list_files(
    message_id: Optional[str] = Query(
        None,
        description="Filtrar por ID de mensaje",
    ),
    thread_id: Optional[str] = Query(
        None,
        description="Filtrar por ID de hilo",
    ),
):
    """
    Lista archivos filtrando por message_id o thread_id.

    Gateway:    GET /api/v1/archivos/?message_id=&thread_id=
    MS archivos: GET /v1/files
    """
    if message_id is None and thread_id is None:
        # replicamos la validación del MS para evitar requests inválidas
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe filtrar por message_id o thread_id",
        )

    try:
        return await archivos_client.list_files(
            message_id=message_id,
            thread_id=thread_id,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al listar archivos")


@router.delete(
    "/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_file(file_id: UUID):
    """
    Marca un archivo como eliminado lógicamente.

    Gateway:    DELETE /api/v1/archivos/{file_id}
    MS archivos: DELETE /v1/files/{file_id}
    """
    try:
        await archivos_client.delete_file(file_id)
        # 204 No Content -> sin body
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al eliminar el archivo")


@router.post(
    "/{file_id}/presign-download",
    response_model=PresignDownloadResponse,
)
async def presign_download(file_id: UUID):
    """
    Genera una URL firmada temporal para descargar el archivo.

    Gateway:    POST /api/v1/archivos/{file_id}/presign-download
    MS archivos: POST /v1/files/{file_id}/presign-download
    """
    try:
        return await archivos_client.presign_download(file_id)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, f"Error al generar URL de descarga: {e}")