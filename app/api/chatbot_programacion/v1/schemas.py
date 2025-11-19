"""
Schemas que usa el GATEWAY para el servicio de chatbot de programación.

Por ahora reutilizamos los modelos del cliente de servicios para mantener consistencia.
"""

from app.services.chatbot_programacion.schemas import (
    HealthResponse,
    QuestionResponse,
    ChatRequest,
    ChatResponse,
)

__all__ = [
    "HealthResponse",
    "QuestionResponse",
    "ChatRequest",
    "ChatResponse",
]
