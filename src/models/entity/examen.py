from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, func
from datetime import datetime

# Elimina las importaciones directas de Pregunta y Resultado
# from src.models.entity.pregunta import Pregunta
# from src.models.entity.resultado import Resultado

if TYPE_CHECKING:
    from src.models.entity.pregunta import Pregunta
    from src.models.entity.resultado import Resultado

class Examen(SQLModel, table=True):
    __tablename__ = "examenes"
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(nullable=False)
    descripcion: Optional[str] = Field(default=None)
    fecha_creacion: datetime = Field(
        sa_column=Column(
            "fecha_creacion",
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )
    preguntas: List["Pregunta"] = Relationship(
        back_populates="examen",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    resultados: List["Resultado"] = Relationship(
        back_populates="examen",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
