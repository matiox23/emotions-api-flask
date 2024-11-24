from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Pregunta(SQLModel, table=True):
    __tablename__ = "preguntas"
    id: Optional[int] = Field(default=None, primary_key=True)
    examen_id: int = Field(foreign_key="examenes.id", nullable=False)
    texto: str = Field(nullable=False)
    # Relaciones diferidas
    examen: "Examen" = Relationship(back_populates="preguntas")
    opciones_respuesta: List["OpcionRespuesta"] = Relationship(back_populates="pregunta", cascade_delete= "all, delete-orphan")
