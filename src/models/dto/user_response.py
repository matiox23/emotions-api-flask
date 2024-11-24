from typing import Optional

from pydantic.v1 import BaseModel, EmailStr, root_validator
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    tipo_usuario: str
    correo: str
    nombre: str
    apellido: Optional[str] = None
    sexo: Optional[str] = None
    fecha_registro: Optional[str] = None

    @root_validator(pre=True)
    def format_fecha_registro(cls, values):
        fecha_registro = values.get('fecha_registro')
        if isinstance(fecha_registro, datetime):
            values['fecha_registro'] = fecha_registro.isoformat()
        return values


    class Config:
        orm_mode = True