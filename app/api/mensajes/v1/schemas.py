# app/api/mensajes/v1/schemas.py
"""
Schemas que usa el GATEWAY para el servicio de mensajes.

Por ahora reutilizamos los modelos del cliente de servicios para mantener
consistencia 1 a 1 con el microservicio de mensajes.
"""

from app.services.mensajes.schemas import (
    MessageCreateIn,
    MessageUpdateIn,
    MessageOut,
    MessagesPageOut,
)

__all__ = [
    "MessageCreateIn",
    "MessageUpdateIn",
    "MessageOut",
    "MessagesPageOut",
]
