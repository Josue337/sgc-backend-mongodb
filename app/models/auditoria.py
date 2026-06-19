from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Union

class SeguimientoModel(BaseModel):
    id_seguimiento: int = Field(..., description="ID numérico único del seguimiento") # [cite: 426]
    id_caso: int = Field(..., description="Relación numérica obligatoria con casos") # [cite: 429]
    id_usuario_cambio: int = Field(..., description="Relación numérica obligatoria con el usuario") # [cite: 430]
    id_estado_nuevo: int = Field(..., description="Relación numérica obligatoria con el nuevo estado") # [cite: 431]
    comentarios: Optional[str] = None # Soporta string o null [cite: 433]
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow) # [cite: 434]

class HistorialCambiosCasosModel(BaseModel):
    id_auditoria: int = Field(..., description="ID numérico único de la auditoría") # [cite: 533]
    id_caso: int = Field(..., description="Relación numérica obligatoria con el caso afectado") # [cite: 534]
    campo_modificado: str # [cite: 535]
    # Soportamos múltiples tipos de datos o null para los valores anteriores y nuevos [cite: 536, 537]
    valor_anterior: Optional[Union[str, int, bool]] = None # [cite: 536]
    valor_nuevo: Optional[Union[str, int, bool]] = None # [cite: 537]
    fecha_cambio: datetime = Field(default_factory=datetime.utcnow) # [cite: 538]
    usuario_db: Optional[str] = None # [cite: 539]