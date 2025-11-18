import httpx

from app.core.config import settings
from app.services.usuarios.schemas import (
    UserRegisterIn,
    UserLoginIn,
    UserUpdateIn,
    UserOut,
    TokenOut,
)

BASE_URL = settings.users_service_base_url.rstrip("/")
REGISTER_URL = f"{BASE_URL}/v1/users/register"
LOGIN_URL = f"{BASE_URL}/v1/auth/login"
ME_URL = f"{BASE_URL}/v1/users/me"


async def register_user(payload: UserRegisterIn) -> UserOut:
    async with httpx.AsyncClient() as client:
        resp = await client.post(REGISTER_URL, json=payload.dict())
        resp.raise_for_status()
        return UserOut(**resp.json())


async def login_user(payload: UserLoginIn) -> TokenOut:
    async with httpx.AsyncClient() as client:
        resp = await client.post(LOGIN_URL, json=payload.dict())
        resp.raise_for_status()
        return TokenOut(**resp.json())


async def get_me(authorization_header: str) -> UserOut:
    """
    Llama a /v1/users/me reenviando el header Authorization tal cual
    (ej: 'Bearer <token>').
    """
    headers = {"Authorization": authorization_header}

    async with httpx.AsyncClient() as client:
        resp = await client.get(ME_URL, headers=headers)
        resp.raise_for_status()
        return UserOut(**resp.json())


async def update_me(authorization_header: str, payload: UserUpdateIn) -> UserOut:
    headers = {"Authorization": authorization_header}

    async with httpx.AsyncClient() as client:
        resp = await client.patch(
            ME_URL,
            headers=headers,
            json=payload.dict(exclude_unset=True),
        )
        resp.raise_for_status()
        return UserOut(**resp.json())
