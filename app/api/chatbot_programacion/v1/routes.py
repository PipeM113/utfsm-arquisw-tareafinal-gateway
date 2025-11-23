import httpx
from fastapi import APIRouter, HTTPException, status

from app.api.chatbot_programacion.v1.schemas import (
    HealthResponse,
    QuestionResponse,
    ChatRequest,
    ChatResponse,
)
from app.services.chatbot_programacion import client as chatbot_client


router = APIRouter(
    tags=["chatbot_programacion"],
)


def _translate_httpx_error(e: httpx.HTTPError, default_message: str) -> HTTPException:
    """
    Traduce errores de httpx (del microservicio) a HTTPException para el cliente del gateway.
    """
    if isinstance(e, httpx.HTTPStatusError) and e.response is not None:
        try:
            body = e.response.json()
            detail = (
                body.get("message")
                or body.get("detail")
                or default_message
            )
        except ValueError:
            detail = default_message
        return HTTPException(
            status_code=e.response.status_code,
            detail=detail,
        )

    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=default_message,
    )


# @router.get(
#     "/health",
#     response_model=HealthResponse,
# )
# async def health():
#     """
#     Verifica que el servicio de chatbot de programación esté operativo.

#     Gateway: GET /api/v1/chatbot-programacion/health
#     MS:      GET /health
#     """
#     try:
#         return await chatbot_client.health()
#     except httpx.HTTPError as e:
#         raise _translate_httpx_error(e, "Error al verificar salud del chatbot")


# @router.get(
#     "/questions",
#     response_model=QuestionResponse,
# )
# async def get_question():
#     """
#     Obtiene una pregunta aleatoria de programación y la publica en la cola.

#     Gateway: GET /api/v1/chatbot-programacion/questions
#     MS:      GET /questions
#     """
#     try:
#         return await chatbot_client.get_question()
#     except httpx.HTTPError as e:
#         raise _translate_httpx_error(e, "Error al obtener pregunta de programación")


# @router.post(
#     "/questions/publish",
#     response_model=QuestionResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def publish_question():
#     """
#     Publica explícitamente una pregunta de programación en la cola.

#     Gateway: POST /api/v1/chatbot-programacion/questions/publish
#     MS:      POST /question/publish
#     """
#     try:
#         return await chatbot_client.publish_question()
#     except httpx.HTTPError as e:
#         raise _translate_httpx_error(e, "Error al publicar pregunta de programación")


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def chat(payload: ChatRequest):
    """
    Envía un mensaje al chatbot de programación (Gemini) y devuelve la respuesta.

    Gateway: POST /api/v1/chatbot-programacion/chat
    MS:      POST /chat
    """
    try:
        return await chatbot_client.chat(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al comunicarse con el chatbot de programación")
