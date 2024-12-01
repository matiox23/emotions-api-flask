# src/models/dto/resultado_response.py

from pydantic import BaseModel
from datetime import datetime

class ResultadoResponseDTO(BaseModel):
    resultado_id: int
    examen_id: int
    puntaje: float
    fecha: str
    usuario_id: int
    nombre: str
    apellido: str
    correo: str
