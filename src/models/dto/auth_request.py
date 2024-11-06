from pydantic.v1 import BaseModel, EmailStr


class AuthRequest(BaseModel):
    correo: EmailStr
    password: str
    tipo_usuario: str
