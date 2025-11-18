"""
Schemas que usa el GATEWAY para el servicio de presencia.

Por ahora reutilizamos los modelos del cliente de servicios para mantener consistencia.
"""

from app.services.presencia.schemas import (
    DeviceEnum,
    StatusEnum,
    UserConnection,
    UserPresence,
    HealthResponse,
    PresenceCreateResponse,
    PresenceListResponse,
    PresenceStatsResponse,
    SinglePresenceResponse,
    StatusUpdateRequest,
    SimpleResponse,
)

__all__ = [
    "DeviceEnum",
    "StatusEnum",
    "UserConnection",
    "UserPresence",
    "HealthResponse",
    "PresenceCreateResponse",
    "PresenceListResponse",
    "PresenceStatsResponse",
    "SinglePresenceResponse",
    "StatusUpdateRequest",
    "SimpleResponse",
]
