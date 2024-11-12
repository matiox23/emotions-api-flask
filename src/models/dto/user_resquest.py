from pydantic.v1 import BaseModel, EmailStr
from datetime import datetime



class UserRequest(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    password: str
    sexo: str
    tipo_usuario: str