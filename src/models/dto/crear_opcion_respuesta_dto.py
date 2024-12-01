from typing import Optional

from pydantic.v1 import BaseModel

class CrearOpcionRespuestaDTO(BaseModel):
    id: Optional[int]  # Agregar id opcional para manejar actualizaciones
    texto: str
    es_correcta: bool = False  # Indica si la opción es la respuesta correcta
