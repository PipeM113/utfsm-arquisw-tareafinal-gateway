"""
Schemas que usa el GATEWAY para el servicio de archivos.

Por ahora reutilizamos los modelos del cliente de servicios para mantener consistencia.
"""

from app.services.archivos.schemas import FileOut, PresignDownloadResponse

__all__ = [
    "FileOut",
    "PresignDownloadResponse",
]
