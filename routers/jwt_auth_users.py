from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------

SECRET_KEY = "super-secret-key-cambiala"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5  # minutos

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 🔐 HASH COMPATIBLE PYTHON 3.14
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# ---------------- MODELOS ----------------

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

# ---------------- DB MOCK ----------------

# password = "123456"
users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@dev.com",
        "disabled": False,
        "password": "$pbkdf2-sha256$29000$rFUqRUhp7X2Pce5dqzUmpA$UzXuhlwVUSyVrfEE.WJXSGFZbwVrG71lkiN9OE0M8H8"
    },
    "glle": {
        "username": "glle",
        "full_name": "Gabriel Marino",
        "email": "glle-design@dev.com",
        "disabled": False,
        "password": "$pbkdf2-sha256$29000$LaU0pvSeE4Lw/j9HqLXW2g$GaYHLZKV/oNV7EhPF7FT7vkhjrJYI7s/gJ3i7Sisg2k"
    }
}

# ---------------- HELPERS ----------------

def search_user_db(username: str) -> UserDB | None:
    if username in users_db:
        return UserDB(**users_db[username])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_minutes: int):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = search_user_db(username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario deshabilitado")

    return user

# ---------------- ENDPOINTS ----------------

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)

    if not user:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")

    if not verify_password(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token(
        data={"sub": user.username},
        expires_minutes=ACCESS_TOKEN_DURATION
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/users/me")
async def me(current_user: User = Depends(get_current_user)):
    return current_user

