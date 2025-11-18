# app/services/archivos/schemas.py
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FileOut(BaseModel):
    id: UUID                      # identificador único del archivo
    filename: str                 # nombre original del archivo
    mime_type: str                # tipo MIME (image/png, application/pdf, etc.)
    size: int                     # tamaño en bytes
    bucket: str                   # nombre del bucket
    object_key: str               # clave/objeto dentro del bucket
    message_id: Optional[str] = None   # id de mensaje asociado (si existe)
    thread_id: Optional[str] = None    # id de hilo asociado (si existe)
    checksum_sha256: str          # hash SHA-256 para integridad
    created_at: datetime          # fecha/hora de creación
    deleted_at: Optional[datetime] = None  # eliminación lógica, si aplica


class PresignDownloadResponse(BaseModel):
    url: str          # URL firmada para descarga
    expires_in: int   # segundos de validez (ej: 3600)
