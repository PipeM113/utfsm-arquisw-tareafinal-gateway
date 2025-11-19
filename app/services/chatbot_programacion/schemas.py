from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    # En /health del servicio de quiz viene además "service"
    service: Optional[str] = None


class QuestionResponse(BaseModel):
    message: str      # mensaje informativo
    question: str     # texto de la pregunta
    question_id: str  # UUID en texto


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str
