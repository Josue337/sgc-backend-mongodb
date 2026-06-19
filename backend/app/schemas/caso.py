from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema base con los campos comunes
class CasoBase(BaseModel):
    titulo_caso: str = Field(..., min_length=3, max_length=100)
    descripcion: str = Field(..., min_length=5)
    prioridad: str = Field(..., description="Alta, Media, Baja")
    id_categoria: int
    id_estado: int

# Esquema para recibir datos al CREAR un caso (Request)
class CasoCreate(CasoBase):
    id_caso: int = Field(..., description="ID numérico único enviado o generado para el caso")
    id_usuario_creador: int
    id_responsable_asignado: Optional[int] = None

# Esquema para recibir datos al ACTUALIZAR un caso (Request - todo opcional)
class CasoUpdate(BaseModel):
    titulo_caso: Optional[str] = None
    descripcion: Optional[str] = None
    prioridad: Optional[str] = None
    id_categoria: Optional[int] = None
    id_estado: Optional[int] = None
    id_responsable_asignado: Optional[int] = None
    activo: Optional[bool] = None

# Esquema de cómo se responde al cliente (Response)
class CasoResponse(CasoBase):
    id_caso: int
    id_usuario_creador: int
    id_responsable_asignado: Optional[int] = None
    fecha_creacion: datetime
    activo: bool

    class Config:
        # Permite mapear diccionarios de Mongo directamente
        from_attributes = True