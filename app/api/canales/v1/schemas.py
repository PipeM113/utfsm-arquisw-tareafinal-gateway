"""
Schemas que usa el GATEWAY para el servicio de canales.

Por ahora, se reutilizan los mismos schemas que el microservicio de canales
"""

from app.services.canales.schemas import (
    Channel,
    ChannelBasicInfoResponse,
    ChannelCreatePayload,
    ChannelIDResponse,
    ChannelMember,
    ChannelType,
    ChannelUpdatePayload,
    ChannelUserPayload,
    ErrorResponse,
)

__all__ = [
    "ChannelType",
    "ChannelMember",
    "ErrorResponse",
    "Channel",
    "ChannelCreatePayload",
    "ChannelUpdatePayload",
    "ChannelBasicInfoResponse",
    "ChannelIDResponse",
    "ChannelUserPayload",
]
