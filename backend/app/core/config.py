from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/backend/app/core -> raíz del repo (donde está .env)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
APP_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
  # URI principal (puede ser mongodb+srv o mongodb estándar)
  MONGO_URI: str = "mongodb://localhost:27017"
  # URI directa sin SRV: evita fallos de DNS en algunas redes
  MONGO_URI_DIRECT: str | None = None
  # Respaldo si Atlas no responde (útil en desarrollo local)
  MONGO_FALLBACK_URI: str = "mongodb://localhost:27017"
  DATABASE_NAME: str = "sgc"
  MONGO_CONNECT_TIMEOUT_MS: int = 8000

  model_config = SettingsConfigDict(
    env_file=(APP_ROOT / ".env", PROJECT_ROOT / ".env"),
    env_file_encoding="utf-8",
  )


settings = Settings()