from pydantic.v1 import BaseModel
from typing import List
from src.models.dto.resultado_response import ResultadoResponseDTO

class ListaResultadosResponseDTO(BaseModel):
    resultados: List[ResultadoResponseDTO]

    class Config:
        orm_mode = True
