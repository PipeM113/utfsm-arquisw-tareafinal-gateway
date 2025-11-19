"""
Schemas que usa el GATEWAY para el servicio de hilos.

Por ahora reutilizamos los modelos del cliente de servicios para mantener consistencia.
"""

from app.services.hilos.schemas import (
    ThreadStatus,
    ThreadCreate,
    ThreadUpdate,
    ThreadOut,
)

__all__ = [
    "ThreadStatus",
    "ThreadCreate",
    "ThreadUpdate",
    "ThreadOut",
]
