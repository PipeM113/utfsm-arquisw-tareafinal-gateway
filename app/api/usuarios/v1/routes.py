from fastapi import APIRouter, HTTPException, status, Header
import httpx

from app.api.usuarios.v1.schemas import (
    UserRegisterIn,
    UserLoginIn,
    UserUpdateIn,
    UserOut,
    TokenOut,
)
from app.services.usuarios import client as usuarios_client

router = APIRouter(
    tags=["usuarios"],
)


def _translate_httpx_error(e: httpx.HTTPError, default_message: str) -> HTTPException:
    """
    Traduce errores de httpx (del microservicio) a HTTPException para el cliente del gateway.
    """
    if isinstance(e, httpx.HTTPStatusError) and e.response is not None:
        try:
            body = e.response.json()
            detail = body.get("message") or body.get("detail") or default_message
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


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(payload: UserRegisterIn):
    """
    Registra un nuevo usuario.

    Gateway:    POST /api/v1/usuarios/register
    MS usuarios: POST /v1/users/register
    """
    try:
        return await usuarios_client.register_user(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al registrar el usuario")


@router.post(
    "/login",
    response_model=TokenOut,
)
async def login_user(payload: UserLoginIn):
    """
    Autentica un usuario y devuelve un token JWT.

    Gateway:    POST /api/v1/usuarios/login
    MS usuarios: POST /v1/auth/login
    """
    try:
        return await usuarios_client.login_user(payload)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al iniciar sesión")


@router.get(
    "/me",
    response_model=UserOut,
)
async def get_me(authorization: str = Header(..., alias="Authorization")):
    """
    Devuelve el perfil del usuario autenticado.

    - El cliente debe enviar Authorization: Bearer <token>
    - El gateway reenvía este header al MS de usuarios.

    Gateway:    GET /api/v1/usuarios/me
    MS usuarios: GET /v1/users/me
    """
    try:
        return await usuarios_client.get_me(authorization_header=authorization)
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al obtener el perfil del usuario")


@router.patch(
    "/me",
    response_model=UserOut,
)
async def update_me(
    payload: UserUpdateIn,
    authorization: str = Header(..., alias="Authorization"),
):
    """
    Actualiza el perfil del usuario autenticado (por ahora solo full_name).

    Gateway:    PATCH /api/v1/usuarios/me
    MS usuarios: PATCH /v1/users/me
    """
    try:
        return await usuarios_client.update_me(
            authorization_header=authorization,
            payload=payload,
        )
    except httpx.HTTPError as e:
        raise _translate_httpx_error(e, "Error al actualizar el perfil del usuario")
