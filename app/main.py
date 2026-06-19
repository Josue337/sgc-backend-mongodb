from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routers import casos, users, maestros

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta antes de que la aplicación empiece a recibir peticiones
    await connect_to_mongo()
    yield
    # Esto se ejecuta cuando la aplicación se está apagando
    await close_mongo_connection()

app = FastAPI(
    title="SGC - Sistema de Gestión y Seguimiento de Casos API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(casos.router)
app.include_router(users.router)
app.include_router(maestros.router)

@app.get("/")
async def root():
    return {"message": "SGC API funcionando correctamente"}