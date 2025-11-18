# app/api/wikipedia/v1/schemas.py
"""
Schemas que usa el GATEWAY para el servicio de Wikipedia.

Por ahora reutilizamos los modelos del cliente de servicios para mantener consistencia.
"""

from app.services.wikipedia.schemas import (
    ChatWikipediaRequest,
    ChatWikipediaResponse,
)

__all__ = [
    "ChatWikipediaRequest",
    "ChatWikipediaResponse",
]
