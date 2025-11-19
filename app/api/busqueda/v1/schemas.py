# app/api/busqueda/v1/schemas.py
"""
Schemas que usa el GATEWAY para el servicio de búsqueda.

Por ahora reutilizamos los modelos del cliente de servicios para mantener
consistencia 1 a 1 con el microservicio.
"""

from app.services.busqueda.schemas import (
    IndexEnum,
    SearchResponse,
)

__all__ = [
    "IndexEnum",
    "SearchResponse",
]
