from typing import List
from pydantic.v1 import BaseModel
from src.models.dto.examen_response_dto import ExamenResponseDTO

class ListaExamenesResponseDTO(BaseModel):
    examenes: List[ExamenResponseDTO]

    class Config:
        orm_mode = True
