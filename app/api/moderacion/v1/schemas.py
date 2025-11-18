"""
Schemas que usa el GATEWAY para el servicio de moderación.

Por ahora reutilizamos los modelos del cliente de servicios para mantener consistencia
"""

from app.services.moderacion.schemas import (
    ModerateMessageRequest,
    ModerateMessageResponse,
    AnalyzeTextRequest,
    AnalyzeTextResponse,
    ModerationStatusResponse,
    AddWordRequest,
    SuccessResponse,
    BlacklistWordsResponse,
    BlacklistStatsResponse,
    BannedUsersResponse,
    UserViolationsResponse,
    UnbanUserRequest,
    UserStatusResponse,
    ChannelStatsResponse,
)

__all__ = [
    "ModerateMessageRequest",
    "ModerateMessageResponse",
    "AnalyzeTextRequest",
    "AnalyzeTextResponse",
    "ModerationStatusResponse",
    "AddWordRequest",
    "SuccessResponse",
    "BlacklistWordsResponse",
    "BlacklistStatsResponse",
    "BannedUsersResponse",
    "UserViolationsResponse",
    "UnbanUserRequest",
    "UserStatusResponse",
    "ChannelStatsResponse",
]
