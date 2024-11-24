from typing import List, Optional
from pydantic.v1 import BaseModel
from src.models.dto.crear_pregunta_dto import CrearPreguntaDTO

class CrearExamenDTO(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    preguntas: List[CrearPreguntaDTO]  # Lista de preguntas asociadas
