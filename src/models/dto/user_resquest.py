from pydantic.v1 import BaseModel, EmailStr

class UserRequest(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    password: str
    sexo: str
    tipo_usuario: str