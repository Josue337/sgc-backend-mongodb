from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RolModel(BaseModel):
    id_rol: int = Field(..., description="ID numérico único del rol") # [cite: 10]
    nombre_rol: str = Field(..., description="Nombre del rol") # [cite: 10]

    class Config:
        json_schema_extra = {
            "example": {
                "id_rol": 1,
                "nombre_rol": "Administrador"
            }
        }

class UsuarioModel(BaseModel):
    id_usuario: int = Field(..., description="ID numérico único del usuario") # [cite: 190]
    nombre: str # [cite: 191]
    documento: str # [cite: 192]
    # EmailStr valida automáticamente el formato ^.+@.+$ que definieron en Mongo [cite: 193]
    correo_electronico: EmailStr 
    contrasena: str  # En la base de datos se guardará ya encriptada (hashed) [cite: 194]
    id_rol: int = Field(..., description="Relación numérica obligatoria con roles") # [cite: 195]

    class Config:
        json_schema_extra = {
            "example": {
                "id_usuario": 1,
                "nombre": "Josue",
                "documento": "123456789",
                "correo_electronico": "josue@example.com",
                "contrasena": "password_hasheado_aqui",
                "id_rol": 1
            }
        }