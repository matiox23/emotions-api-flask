from pydantic.v1 import BaseModel

class CrearOpcionRespuestaDTO(BaseModel):
    texto: str
    es_correcta: bool = False  # Indica si la opción es la respuesta correcta
