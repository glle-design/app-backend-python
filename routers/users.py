from fastapi import APIRouter,HTTPException          # Importamos APIRouter y Excepciones
import uvicorn                                       # Servidor
from pydantic import BaseModel                       # Importar para crear una Identidad

router = APIRouter()

# cd C:\Users\Gabriel\Desktop\python_API\FastAPI
# INICIALIZAR SERVIDOR: python -m uvicorn users:app --reload

# Definimos una Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# Creamos Usuarios con un Objeto
users_list = [User(id = 1, name = "Brais", surname = "Moure", url = "https://moure.dev", age = 40),
              User(id = 2, name = "Gabriel", surname = "Marino", url = "https://gabriel.dev", age = 35),
              User(id = 3 ,name = "Lionel", surname="Messi", url = "https://lio.dev", age = 20)]

# GET: Completo
@router.get("/users")
async def users():
    return users_list

# GET: Individual
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)
    
# Post: Añadir usuarios
@router.post("/user/", response_model=User ,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204,detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user


# Put: Update: Actualizar Usuarios
@router.put("/user/")
async def user(user: User):
    found = False           # Variable para saber si está actualizado el usuario
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user


# Delete: Borrar Usuario
@router.delete("/user/{id}")
async def user(id: int):
    found = False           
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] 
            found = True
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    

        
# Funciones
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}


# Llamr por Query: Llama por un parámetro /?id=1




