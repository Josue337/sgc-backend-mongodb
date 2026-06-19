from datetime import datetime, timedelta
import jwt
import bcrypt
from app.core.config import settings

SECRET_KEY = getattr(settings, "JWT_SECRET", "super_secret_key_para_el_sgc_123456")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def obtener_contrasena_hasheada(password: str) -> str:
    # 1. Convertimos el string a bytes
    password_bytes = password.encode('utf-8')
    
    # 2. Generamos el salt y el hash usando bcrypt nativo
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # 3. Guardamos en la base de datos como un string (texto) limpio
    return hashed.decode('utf-8')

def verificar_contrasena(plain_password: str, hashed_password: str) -> bool:
    try:
        # Convertimos ambos a bytes para que bcrypt pueda compararlos
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

def crear_token_acceso(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt