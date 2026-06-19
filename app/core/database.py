from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger("uvicorn.error")

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_client = MongoDB()

async def connect_to_mongo():
    """Inicializa la conexión con MongoDB Atlas / Local."""
    try:
        db_client.client = AsyncIOMotorClient(settings.MONGO_URI)
        db_client.db = db_client.client[settings.DATABASE_NAME]
        
        # Hacemos un ping rápido para verificar que la conexión sea exitosa
        await db_client.client.admin.command('ping')
        logger.info("✅ Conexión exitosa a MongoDB establecida.")
    except Exception as e:
        logger.error(f"❌ Error al conectar a MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Cierra la conexión con MongoDB."""
    if db_client.client:
        db_client.client.close()
        logger.info("🛑 Conexión a MongoDB cerrada.")

def get_database():
    """Dependency injection para obtener la base de datos en los endpoints."""
    return db_client.db

async def get_next_sequence_value(sequence_name: str, db) -> int:
    """Genera un ID numérico autoincremental usando una colección de contadores."""
    resultado = await db["contador_secuencias"].find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"valor_secuencial": 1}},
        upsert=True,
        return_document=True
    )