from fastapi import FastAPI

from app.core.config import settings
from app.api.canales.v1 import routes as canales_v1
from app.api.usuarios.v1 import routes as usuarios_v1


app = FastAPI(title=settings.app_name)


@app.get("/")
def read_root():
    return {
        "message": "Hola mundo desde el API Gateway",
        "environment": settings.environment,
    }


app.include_router(canales_v1.router, prefix="/api/v1/canales")
app.include_router(usuarios_v1.router, prefix="/api/v1/usuarios")
