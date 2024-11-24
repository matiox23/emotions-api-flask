from pydantic.v1 import BaseModel


class OpcionRespuestaResponse(BaseModel):
    id: int
    texto: str
    es_correcta: bool

    class Config:
        orm_mode = True