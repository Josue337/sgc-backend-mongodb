from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Union

class EstadoModel(BaseModel):
    id_estado: int = Field(..., description="ID numérico único del estado") # [cite: 69]
    nombre_estado: str = Field(..., description="Nombre del estado") # [cite: 73]

class CategoriaModel(BaseModel):
    id_categoria: int = Field(..., description="ID numérico único de la categoría") # [cite: 134]
    nombre_categoria: str = Field(..., description="Nombre de la categoría") # [cite: 135]

class CasoModel(BaseModel):
    id_caso: int = Field(..., description="ID numérico único del caso") # [cite: 290]
    titulo_caso: str # [cite: 291]
    descripcion: str # [cite: 292]
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow) # [cite: 293]
    prioridad: str # [cite: 294]
    id_categoria: int = Field(..., description="Relación numérica obligatoria con categorías") # [cite: 295]
    id_estado: int = Field(..., description="Relación numérica obligatoria con estados") # [cite: 296]
    id_usuario_creador: int = Field(..., description="Relación numérica obligatoria con usuarios") # [cite: 297]
    # Usamos Optional e int | None para soportar que sea entero o null como en su esquema [cite: 298]
    id_responsable_assigned: Optional[int] = Field(None, description="Relación numérica opcional con usuarios") # [cite: 298]
    activo: bool = Field(True) # [cite: 299]