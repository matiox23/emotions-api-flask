from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.models.entity.examen import Examen
    from src.models.entity.opcion_respuesta import OpcionRespuesta
    from src.models.entity.respuesta_detalle import RespuestaDetalle

class Pregunta(SQLModel, table=True):
    __tablename__ = "preguntas"
    id: Optional[int] = Field(default=None, primary_key=True)
    examen_id: int = Field(foreign_key="examenes.id", nullable=False)
    texto: str = Field(nullable=False)
    # Relaciones diferidas
    examen: "Examen" = Relationship(back_populates="preguntas")
    opciones_respuesta: List["OpcionRespuesta"] = Relationship(back_populates="pregunta",
                                                               sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    respuestas_detalle: List["RespuestaDetalle"] = Relationship(
        back_populates="pregunta",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

