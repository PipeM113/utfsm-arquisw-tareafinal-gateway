from dataclasses import dataclass
import os


@dataclass
class Settings:
    app_name: str = "UTFSM Arquitectura - API Gateway"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Canales
    channels_service_base_url: str = os.getenv(
        "CHANNELS_SERVICE_BASE_URL",
        "https://channel-api.inf326.nur.dev",
    )

    # Usuarios
    users_service_base_url: str = os.getenv(
        "USERS_SERVICE_BASE_URL",
        "https://users.inf326.nursoft.dev",
    )

    # Mensajes
    messages_service_base_url: str = os.getenv(
        "MESSAGES_SERVICE_BASE_URL",
        "https://messages-service.kroder.dev",
    )

    # Moderación
    moderation_service_base_url: str = os.getenv(
        "MODERATION_SERVICE_BASE_URL",
        "https://moderation.inf326.nur.dev",
    )

    # Presencia
    presence_service_base_url: str = os.getenv(
        "PRESENCE_SERVICE_BASE_URL",
        "https://moderation.inf326.nur.dev",
    )

    # Chatbot Wikipedia
    wikipedia_service_base_url: str = os.getenv(
        "WIKIPEDIA_SERVICE_BASE_URL",
        "http://wikipedia-chatbot-134-199-176-197.nip.io",
    )

    # Archivos
    files_service_base_url: str = os.getenv(
        "FILES_SERVICE_BASE_URL",
        "http://files-service",
    )

    # Chatbot de Programación
    chatbot_programacion_service_base_url: str = os.getenv(
        "CHATBOT_PROGRAMACION_SERVICE_BASE_URL",
        "https://chatbotprogra.inf326.nursoft.dev",
    )


settings = Settings()
