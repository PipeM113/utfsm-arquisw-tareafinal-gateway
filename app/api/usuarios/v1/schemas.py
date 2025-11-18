# app/api/usuarios/v1/schemas.py
"""
Schemas que usa el GATEWAY para el servicio de usuarios.

Por ahora reutilizamos los modelos del cliente de servicios para mantener
consistencia 1 a 1 con el microservicio de usuarios.
Más adelante, si el gateway necesita adaptar algo, podemos definir modelos
propios aquí.
"""

from app.services.usuarios.schemas import (
    UserRegisterIn,
    UserLoginIn,
    UserUpdateIn,
    UserOut,
    TokenOut,
    ErrorOut,
)

__all__ = [
    "UserRegisterIn",
    "UserLoginIn",
    "UserUpdateIn",
    "UserOut",
    "TokenOut",
    "ErrorOut",
]
