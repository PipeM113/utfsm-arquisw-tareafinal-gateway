"""
Schemas que usa el GATEWAY para el servicio de archivos.

Por ahora reutilizamos los modelos del cliente de servicios para mantener consistencia.
"""

from app.services.archivos.schemas import FileOut, PresignDownloadResponse
from pydantic import BaseModel

__all__ = [
    "FileOut",
    "PresignDownloadResponse",
]

class PresignDownloadRequest(BaseModel):
    """Schema para solicitar URL firmada de descarga de archivo."""
    file_url: str  # URL interna del archivo