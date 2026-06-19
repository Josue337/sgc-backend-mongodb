from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    documento: str
    correo_electronico: EmailStr
    id_rol: int

class UsuarioCreate(UsuarioBase):
    id_usuario: int = Field(..., description="ID numérico único")
    contrasena: str = Field(..., min_length=6)

class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id_usuario: Optional[int] = None
    correo: Optional[str] = None

class LoginRequest(BaseModel):
    correo_electronico: str
    contrasena: str