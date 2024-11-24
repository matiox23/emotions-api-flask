from pydantic.v1 import BaseModel
from typing import List

class RespuestaDTO(BaseModel):
    pregunta_id: int
    opcion_id: int

class ResultadoRequest(BaseModel):
    usuario_id: int
    respuestas: List[RespuestaDTO]
