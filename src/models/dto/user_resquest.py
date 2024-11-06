from pydantic.v1 import BaseModel, EmailStr


class UserRequest(BaseModel):
    nombre: str
    correo: EmailStr
    password: str
    tipo_usuario: str