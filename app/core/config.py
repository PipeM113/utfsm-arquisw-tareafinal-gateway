from dataclasses import dataclass
import os


@dataclass
class Settings:
    app_name: str = "UTFSM Arquitectura - API Gateway"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # URL base del microservicio de Canales
    channels_service_base_url: str = os.getenv(
        "CHANNELS_SERVICE_BASE_URL",
        "https://channel-api.inf326.nur.dev",
    )

    # URL base del microservicio de Usuarios
    users_service_base_url: str = os.getenv(
        "USERS_SERVICE_BASE_URL",
        "https://users.inf326.nursoft.dev",
    )


settings = Settings()
