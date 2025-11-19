from fastapi import FastAPI

from app.core.config import settings
from app.api.canales.v1 import routes as canales_v1
from app.api.usuarios.v1 import routes as usuarios_v1
from app.api.mensajes.v1 import routes as mensajes_v1
from app.api.moderacion.v1 import routes as moderacion_v1
from app.api.presencia.v1 import routes as presencia_v1
from app.api.wikipedia.v1 import routes as wikipedia_v1
from app.api.archivos.v1 import routes as archivos_v1
from app.api.chatbot_programacion.v1 import routes as chatbot_v1
from app.api.busqueda.v1 import routes as busqueda_v1


app = FastAPI(title=settings.app_name)


@app.get("/")
def read_root():
    return {
        "message": "Hola mundo desde el API Gateway",
        "environment": settings.environment,
    }


# Versión 1 de la API: montamos servicios
app.include_router(canales_v1.router, prefix="/api/v1/canales")
app.include_router(usuarios_v1.router, prefix="/api/v1/usuarios")
app.include_router(mensajes_v1.router, prefix="/api/v1/mensajes")
app.include_router(moderacion_v1.router, prefix="/api/v1/moderacion")
app.include_router(presencia_v1.router, prefix="/api/v1/presencia")
app.include_router(wikipedia_v1.router, prefix="/api/v1/wikipedia")
app.include_router(archivos_v1.router, prefix="/api/v1/archivos")
app.include_router(chatbot_v1.router, prefix="/api/v1/chatbot")
app.include_router(busqueda_v1.router, prefix="/api/v1/busqueda")
