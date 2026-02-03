from fastapi import FastAPI                       # Importamos FasAPI
import uvicorn                                    # Importamos Servidor
from  routers import products, users, basic_auth_users, jwt_auth_users, user_db            # Importamos Rutas del Productos y Usuarios
from fastapi.staticfiles import StaticFiles       # Importamos fastapi más el módulo de archivos estáticos


app = FastAPI()                          # Inicializamos Objeto FastAPI

# Routers
app.include_router(products.router)      # Incluimos la rutas de Productos
app.include_router(users.router)         # Incuimos la ruta de Usuarios
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
# Incluimos el router
app.include_router(user_db.router)


# cd C:/Users/Gabriel/Desktop/python_API/FastAPI
# INICIALIZAR SERVIDOR: python -m uvicorn main:app --reload

@app.get("/")
async def root():
    return {"message": "API Conectada con MongoDB"}

@app.get("/")                            # Creamos la ruta get para accder a la web
async def root():                        # Hacemos una función asyncrona
    return "FastAPI Funcionando desde Python"   # Retornamos la función 


@app.get("/url")
async def url():
    return {"url_curso":"https://glledev.com/python"}



