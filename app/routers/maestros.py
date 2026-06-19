from fastapi import APIRouter, Depends
from app.core.database import get_database
from app.schemas.maestros import EstadoResponse, CategoriaResponse
from typing import List

router = APIRouter(prefix="/maestros", tags=["Tablas Maestras (Configuraciones)"])

@router.get("/estados", response_model=List[EstadoResponse])
async def listar_estados(db = Depends(get_database)):
    """Retorna todos los estados disponibles para los casos (ej: Abierto, En Proceso, Cerrado)."""
    cursor = db["estados"].find()
    estados = await cursor.to_list(length=100)
    return estados

@router.get("/categorias", response_model=List[CategoriaResponse])
async def listar_categorias(db = Depends(get_database)):
    """Retorna todas las categorías disponibles (ej: Hardware, Software, Redes)."""
    cursor = db["categorias"].find()
    categorias = await cursor.to_list(length=100)
    return categorias