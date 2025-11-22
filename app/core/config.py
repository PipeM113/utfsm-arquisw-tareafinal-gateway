from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    app_name: str = "UTFSM Arquitectura - API Gateway"
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Canales
    channels_service_base_url: str = os.getenv(
        "CHANNELS_SERVICE_BASE_URL",
        "https://channels.example.com",
    )

    # Usuarios
    users_service_base_url: str = os.getenv(
        "USERS_SERVICE_BASE_URL",
        "https://users.example.com",
    )

    # Mensajes
    messages_service_base_url: str = os.getenv(
        "MESSAGES_SERVICE_BASE_URL",
        "https://messages.example.com",
    )

    # Moderación
    moderation_service_base_url: str = os.getenv(
        "MODERATION_SERVICE_BASE_URL",
        "https://moderation.example.com",
    )

    # Presencia
    presence_service_base_url: str = os.getenv(
        "PRESENCE_SERVICE_BASE_URL",
        "https://presence.example.com",
    )

    # Chatbot Wikipedia
    wikipedia_service_base_url: str = os.getenv(
        "WIKIPEDIA_SERVICE_BASE_URL",
        "https://wikipedia-chatbot.example.com",
    )

    # Archivos
    files_service_base_url: str = os.getenv(
        "FILES_SERVICE_BASE_URL",
        "https://files.example.com",
    )

    # Chatbot de programación
    chatbot_service_base_url: str = os.getenv(
        "CHATBOT_SERVICE_BASE_URL",
        "https://chatbotprogra.example.com",
    )

    # Búsqueda
    search_service_base_url: str = os.getenv(
        "SEARCH_SERVICE_BASE_URL",
        "https://searchservice.example.com",
    )

    # Hilos
    threads_service_base_url: str = os.getenv(
        "THREADS_SERVICE_BASE_URL",
        "https://threads.example.com",
    )

    #CORS
    cors_allowed_origins: str = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "*",   
    )


settings = Settings()
