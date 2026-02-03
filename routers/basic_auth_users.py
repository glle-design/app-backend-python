from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



#Arrancar Servidor
# cd C:\Users\Gabriel\Desktop\python_API\FastAPI\routers
# python -m uvicorn basic_auth_users:app --reload

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# -------- MODELOS --------

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


# -------- BASE DE DATOS --------

users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@dev.com",
        "disabled": False,
        "password": "123456"
    },
    "glle": {
        "username": "glle",
        "full_name": "Gabriel Marino",
        "email": "glle-design@dev.com",
        "disabled": True,
        "password": "holapython"
    }
}


# -------- UTILIDADES --------

def search_user_db(username: str):            # Búsqueda de usuarios
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    user_db = search_user_db(username)
    if user_db:
        return User(**user_db.dict(exclude={"password"}))


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


# -------- ENDPOINTS --------

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")

    if form.password != user.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {
        "access_token": user.username,
        "token_type": "bearer"
    }


@router.get("/users/me", response_model=User)
async def me(user: User = Depends(current_user)):
    return user

