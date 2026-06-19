from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from app.core.database import get_database
from app.core.security import obtener_contrasena_hasheada, verificar_contrasena, crear_token_acceso, SECRET_KEY, ALGORITHM
from app.schemas.user import UsuarioCreate, UsuarioResponse, Token, TokenData, LoginRequest

router = APIRouter(prefix="/auth", tags=["Autenticación e Inicios de Sesión"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form-swagger")

# 1. RUTA DE REGISTRO (La que se había borrado)
@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(usuario: UsuarioCreate, db = Depends(get_database)):
    existe_id = await db["usuarios"].find_one({"id_usuario": usuario.id_usuario})
    existe_correo = await db["usuarios"].find_one({"correo_electronico": usuario.correo_electronico})
    
    if existe_id or existe_correo:
        raise HTTPException(status_code=400, detail="El ID de usuario o el correo electrónico ya están registrados.")
    
    usuario_dict = usuario.model_dump()
    usuario_dict["contrasena"] = obtener_contrasena_hasheada(usuario.contrasena)
    
    await db["usuarios"].insert_one(usuario_dict)
    return usuario_dict

# 2. RUTA DE LOGIN PARA EL FRONTEND (JSON)
@router.post("/login", response_model=Token)
async def login(credenciales: LoginRequest, db = Depends(get_database)):
    usuario = await db["usuarios"].find_one({"correo_electronico": credenciales.correo_electronico})
    if not usuario:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    if not verificar_contrasena(credenciales.contrasena, usuario["contrasena"]):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    token_acceso = crear_token_acceso(
        data={"sub": str(usuario["id_usuario"]), "correo": usuario["correo_electronico"]}
    )
    return {"access_token": token_acceso, "token_type": "bearer"}

# 3. RUTA DE SOPORTE PARA EL BOTÓN "AUTHORIZE" DE SWAGGER
@router.post("/login-form-swagger", response_model=Token, include_in_schema=False)
async def login_para_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_database)):
    usuario = await db["usuarios"].find_one({"correo_electronico": form_data.username})
    if not usuario:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    if not verificar_contrasena(form_data.password, usuario["contrasena"]):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    token_acceso = crear_token_acceso(
        data={"sub": str(usuario["id_usuario"]), "correo": usuario["correo_electronico"]}
    )
    return {"access_token": token_acceso, "token_type": "bearer"}

# 4. DEPENDENCIA PARA PROTEGER OTRAS RUTAS
async def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de acceso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario: int = int(payload.get("sub"))
        if id_usuario is None:
            raise credentials_exception
        token_data = TokenData(id_usuario=id_usuario, correo=payload.get("correo"))
    except jwt.PyJWTError:
        raise credentials_exception
        
    usuario = await db["usuarios"].find_one({"id_usuario": token_data.id_usuario})
    if usuario is None:
        raise credentials_exception
    return usuario