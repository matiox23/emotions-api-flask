from typing import Optional, List
from pydantic.v1 import BaseModel, root_validator
from datetime import datetime

from src.models.dto.PreguntaResponseDTO import PreguntaResponseDTO

class ExamenResponseDTO(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_creacion: Optional[str] = None
    preguntas: List[PreguntaResponseDTO]

    @root_validator(pre=True)
    def format_fecha_creacion(cls, values):
        fecha_creacion = values.get('fecha_creacion')
        if isinstance(fecha_creacion, datetime):
            values['fecha_creacion'] = fecha_creacion.isoformat()
        return values

    class Config:
        orm_mode = True
