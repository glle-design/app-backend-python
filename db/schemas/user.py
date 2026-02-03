def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]), # Crucial: convertir ObjectId a string
        "username": user["username"],
        "email": user["email"]
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
