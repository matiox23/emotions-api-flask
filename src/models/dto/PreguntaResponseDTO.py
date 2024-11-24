
from typing import List
from pydantic.v1 import BaseModel
from src.models.dto.OpcionRespuestaResponseDTO import OpcionRespuestaResponseDTO

class PreguntaResponseDTO(BaseModel):
    id: int
    texto: str
    opciones_respuesta: List[OpcionRespuestaResponseDTO]


class PreguntaResponseDTO(BaseModel):
    id: int  # ID único de la pregunta
    texto: str  # Texto de la pregunta
    opciones_respuesta: List[OpcionRespuestaResponseDTO]  # Lista de opciones de respuesta asociadas