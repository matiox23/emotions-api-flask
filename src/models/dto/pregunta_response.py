
from pydantic.v1 import BaseModel
from typing import List, Optional

from src.models.dto.opcion_respuesta_response import OpcionRespuestaResponse


class PreguntaResponse(BaseModel):
    id: int
    texto: str
    opciones_respuesta: List[OpcionRespuestaResponse]

    class Config:
        orm_mode = True