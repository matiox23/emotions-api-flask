from typing import List, Optional
from pydantic.v1 import BaseModel
from src.models.dto.crear_opcion_respuesta_dto import CrearOpcionRespuestaDTO

class CrearPreguntaDTO(BaseModel):
    id: Optional[int]
    texto: str
    opciones_respuesta: List[CrearOpcionRespuestaDTO]  # Lista de opciones de respuesta asociadas
