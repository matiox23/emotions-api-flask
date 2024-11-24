from pydantic.v1 import BaseModel

class OpcionRespuestaResponseDTO(BaseModel):
    id: int  # ID único de la opción de respuesta
    texto: str  # Texto de la opción de respuesta
    es_correcta: bool  # Indica si es la respuesta correcta
