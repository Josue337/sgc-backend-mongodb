from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from app.core.config import settings
import logging

logger = logging.getLogger("uvicorn.error")

SEQUENCE_SOURCES = {
    "id_auditoria": ("historial_cambios_casos", "id_auditoria"),
    "id_seguimiento": ("seguimiento", "id_seguimiento"),
}

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_client = MongoDB()

def _mask_mongo_uri(uri: str) -> str:
    if "@" not in uri:
        return uri
    scheme, rest = uri.split("://", 1)
    creds, host = rest.split("@", 1)
    user = creds.split(":", 1)[0]
    return f"{scheme}://{user}:****@{host}"

def _mongo_uris_to_try() -> list[str]:
    uris: list[str] = []
    for uri in (settings.MONGO_URI_DIRECT, settings.MONGO_URI, settings.MONGO_FALLBACK_URI):
        if uri and uri not in uris:
            uris.append(uri)
    return uris

async def _connect_client(uri: str) -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(
        uri,
        serverSelectionTimeoutMS=settings.MONGO_CONNECT_TIMEOUT_MS,
    )
    await client.admin.command("ping")
    return client

async def sync_sequence_counters(db):
    """Alinea los contadores con el máximo ID ya existente en cada colección."""
    for sequence_name, (collection_name, field_name) in SEQUENCE_SOURCES.items():
        max_doc = await db[collection_name].find_one(sort=[(field_name, -1)])
        max_value = max_doc[field_name] if max_doc else 0
        current = await db["contador_secuencias"].find_one({"_id": sequence_name})
        current_value = current.get("valor_secuencial", 0) if current else 0

        if current_value < max_value:
            await db["contador_secuencias"].update_one(
                {"_id": sequence_name},
                {"$set": {"valor_secuencial": max_value}},
                upsert=True,
            )
            logger.info(
                "Contador '%s' sincronizado: %s -> %s",
                sequence_name,
                current_value,
                max_value,
            )

async def connect_to_mongo():
    """Inicializa la conexión con MongoDB Atlas / Local."""
    last_error = None

    for uri in _mongo_uris_to_try():
        try:
            db_client.client = await _connect_client(uri)
            db_client.db = db_client.client[settings.DATABASE_NAME]
            logger.info(
                "✅ Conexión exitosa a MongoDB (%s).",
                _mask_mongo_uri(uri),
            )
            break
        except Exception as exc:
            last_error = exc
            logger.warning(
                "No se pudo conectar con %s: %s",
                _mask_mongo_uri(uri),
                exc,
            )
    else:
        logger.error("❌ No fue posible conectar a ninguna URI de MongoDB.")
        raise last_error

    try:
        await sync_sequence_counters(db_client.db)

        # Sembrar datos semilla de Estados si no existen
        estados_count = await db_client.db["estados"].count_documents({})
        if estados_count == 0:
            await db_client.db["estados"].insert_many([
                {"id_estado": 1, "nombre_estado": "Abierto"},
                {"id_estado": 2, "nombre_estado": "En Proceso"},
                {"id_estado": 3, "nombre_estado": "Cerrado"}
            ])
            logger.info("🌱 Estados sembrados por defecto en MongoDB.")

        # Sembrar datos semilla de Categorías si no existen
        categorias_count = await db_client.db["categorias"].count_documents({})
        if categorias_count == 0:
            await db_client.db["categorias"].insert_many([
                {"id_categoria": 1, "nombre_categoria": "Hardware"},
                {"id_categoria": 2, "nombre_categoria": "Software"},
                {"id_categoria": 3, "nombre_categoria": "Redes"}
            ])
            logger.info("🌱 Categorías sembradas por defecto en MongoDB.")

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
        return_document=ReturnDocument.AFTER,
    )
    return resultado["valor_secuencial"]
