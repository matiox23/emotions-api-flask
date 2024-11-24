from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class OpcionRespuesta(SQLModel, table=True):
    __tablename__ = "opciones_respuesta"
    id: Optional[int] = Field(default=None, primary_key=True)
    pregunta_id: int = Field(foreign_key="preguntas.id", nullable=False)
    texto: str = Field(nullable=False)
    es_correcta: bool = Field(default=False)

    # Relaciones diferidas
    pregunta: "Pregunta" = Relationship(back_populates="opciones_respuesta")
