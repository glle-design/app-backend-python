from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@router.get("/", response_model=list[User])
async def get_users():
    return users_schema(db_client.users.find())

@router.get("/{id}", response_model=User)
async def get_user_by_id(id: str):
    return search_user("_id", ObjectId(id))

# Post: Añadir usuarios
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    # 1. Verificamos si ya existe por email (opcional pero recomendado)
    if db_client.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El email ya está registrado"
        )

    # 2. Convertimos el modelo Pydantic a diccionario
    user_dict = dict(user)
    
    # 3. Eliminamos el campo 'id' para que MongoDB cree su propio '_id'
    del user_dict["id"]
    
    # 4. Insertamos en la base de datos
    # Usamos .users si db_client ya apunta a la base de datos local
    result = db_client.users.insert_one(user_dict)
    
    # 5. Buscamos el usuario recién creado usando el ID generado
    new_user_db = db_client.users.find_one({"_id": result.inserted_id})
    
    # 6. Lo pasamos por el schema y lo devolvemos como modelo User
    return User(**user_schema(new_user_db))

@router.put("/", response_model=User)
async def update_user(user: User):
    # 1. Convertimos a diccionario y extraemos el ID
    user_dict = dict(user)
    user_id = user_dict.get("id")

    # 2. Validamos que el ID no sea nulo antes de operar
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Se requiere el ID del usuario para actualizar"
        )

    # 3. Limpiamos el diccionario para la base de datos
    del user_dict["id"]

    try:
        # 4. Intentamos la actualización
        # Usamos ObjectId(user_id) para que Mongo lo entienda
        result = db_client.users.find_one_and_replace(
            {"_id": ObjectId(user_id)}, 
            user_dict, 
            return_document=True # Para que devuelva el objeto actualizado
        )
    except Exception:
        # Este error ocurre si el user_id no tiene formato de ObjectId válido
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El formato del ID proporcionado es inválido"
        )

    # 5. Si no hubo error de formato pero no encontró el documento
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontró ningún usuario con ese ID para actualizar"
        )

    # 6. Devolvemos el usuario procesado por el schema
    return User(**user_schema(result))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=404, detail="No se ha encontrado el usuario")

# Helper
def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")





