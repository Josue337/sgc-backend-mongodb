from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/backend/app/core -> raíz del repo (donde está .env)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
APP_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Reemplaza con tu cadena de conexión local o de MongoDB Atlas en el archivo .env
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "sgc"

    model_config = SettingsConfigDict(
        env_file=(APP_ROOT / ".env", PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()