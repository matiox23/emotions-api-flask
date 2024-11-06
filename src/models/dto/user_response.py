from pydantic.v1 import BaseModel, EmailStr


class UserResponse(BaseModel):
    id:int
    nombre: str
    correo: EmailStr
    tipo_usuario: str

    class Config:
        orm_mode = True