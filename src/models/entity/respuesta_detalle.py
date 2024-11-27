from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from src.models.entity.pregunta import Pregunta
    from src.models.entity.resultado import Resultado


class RespuestaDetalle(SQLModel, table=True):
    __tablename__ = "respuestas_detalle"
    id: Optional[int] = Field(default=None, primary_key=True)
    resultado_id: int = Field(foreign_key="resultados.id", nullable=False)
    pregunta_id: int = Field(foreign_key="preguntas.id", nullable=False)
    correcta: bool = Field(nullable=False)

    resultado: "Resultado" = Relationship(back_populates="detalles")
    pregunta: "Pregunta" = Relationship(back_populates="respuestas_detalle")
