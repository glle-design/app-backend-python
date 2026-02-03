from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None  # MongoDB usa strings para el ID en el cliente
    username: str
    email: str