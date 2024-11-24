from typing import List
from pydantic.v1 import BaseModel
from src.models.dto.crear_opcion_respuesta_dto import CrearOpcionRespuestaDTO

class CrearPreguntaDTO(BaseModel):
    texto: str
    opciones_respuesta: List[CrearOpcionRespuestaDTO]  # Lista de opciones de respuesta asociadas
