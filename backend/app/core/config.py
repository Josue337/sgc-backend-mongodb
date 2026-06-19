from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Reemplaza con tu cadena de conexión local o de MongoDB Atlas en el archivo .env
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "sgc"
    
    class Config:
        env_file = ".env"

settings = Settings()