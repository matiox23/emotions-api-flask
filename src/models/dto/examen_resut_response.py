from pydantic.v1 import BaseModel, root_validator
from datetime import datetime

class ResultadoExamenResponseDTO(BaseModel):
    id: int
    usuario_id: int
    examen_id: int
    puntaje: int
    fecha: str  # Ahora la fecha será un string con formato ISO

    @root_validator(pre=True)
    def format_fecha(cls, values):
        fecha = values.get('fecha')
        if isinstance(fecha, datetime):
            values['fecha'] = fecha.isoformat()
        return values

    class Config:
        orm_mode = True
