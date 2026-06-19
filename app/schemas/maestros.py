from pydantic import BaseModel, Field

# --- ESTADOS ---
class EstadoBase(BaseModel):
    nombre_estado: str = Field(..., max_length=50)

class EstadoResponse(EstadoBase):
    id_estado: int

    class Config:
        from_attributes = True

# --- CATEGORIAS ---
class CategoriaBase(BaseModel):
    nombre_categoria: str = Field(..., max_length=50)

class CategoriaResponse(CategoriaBase):
    id_categoria: int

    class Config:
        from_attributes = True