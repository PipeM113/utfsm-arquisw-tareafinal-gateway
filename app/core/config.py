from dataclasses import dataclass
import os


@dataclass
class Settings:
    app_name: str = "UTFSM Arquitectura - API Gateway"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # URL base del microservicio de canales
    channels_service_base_url: str = os.getenv(
        "CHANNELS_SERVICE_BASE_URL",
        "https://channel-api.inf326.nur.dev",
    )


settings = Settings()
