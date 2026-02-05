from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from pymongo import ReturnDocument

from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={404: {"description": "No encontrado"}}
)

# -------------------------
# GET ALL USERS
# -------------------------
@router.get("/", response_model=list[User])
async def get_users():
    return users_schema(db_client.users.find())

# -------------------------
# GET USER BY ID
# -------------------------
@router.get("/{id}", response_model=User)
async def get_user_by_id(id: str):
    return search_user("_id", id)

# -------------------------
# CREATE USER
# -------------------------
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):

    if db_client.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    user_dict = user.model_dump()
    user_dict.pop("id", None)

    result = db_client.users.insert_one(user_dict)
    new_user = db_client.users.find_one({"_id": result.inserted_id})

    return User(**user_schema(new_user))

# -------------------------
# UPDATE USER
# -------------------------
@router.put("/{id}", response_model=User)
async def update_user(id: str, user: User):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )

    user_dict = user.model_dump()
    user_dict.pop("id", None)

    updated_user = db_client.users.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": user_dict},
        return_document=ReturnDocument.AFTER
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return User(**user_schema(updated_user))

# -------------------------
# DELETE USER
# -------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )

    deleted = db_client.users.find_one_and_delete(
        {"_id": ObjectId(id)}
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return None

# -------------------------
# HELPER
# -------------------------
def search_user(field: str, value: str):

    if field == "_id":
        if not ObjectId.is_valid(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID inválido"
            )
        value = ObjectId(value)

    user = db_client.users.find_one({field: value})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return User(**user_schema(user))
