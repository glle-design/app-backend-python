from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from routers import (
    products,
    users,
    basic_auth_users,
    jwt_auth_users,
    user_db
)

app = FastAPI(
    title="FastAPI + MongoDB API",
    version="1.0.0"
)

# -------------------------
# Routers
# -------------------------
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(user_db.router)

# -------------------------
# Static files
# -------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------
# Root & Health
# -------------------------
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "API funcionando correctamente",
        "database": "MongoDB"
    }

@app.get("/health")
async def health_check():
    return {
        "service": "FastAPI",
        "status": "running"
    }

@app.get("/url")
async def get_course_url():
    return {
        "url_curso": "https://glledev.com/python"
    }

# -------------------------
# Run local
# -------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
