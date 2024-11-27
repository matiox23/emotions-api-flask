from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, func
from datetime import datetime

if TYPE_CHECKING:
    from src.models.entity.user import User
    from src.models.entity.examen import Examen
    from src.models.entity.respuesta_detalle import RespuestaDetalle

class Resultado(SQLModel, table=True):
    __tablename__ = "resultados"
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="users.id", nullable=False)
    examen_id: int = Field(foreign_key="examenes.id", nullable=False)
    puntaje: int = Field(nullable=False)
    fecha: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relaciones diferidas
    user: "User" = Relationship(back_populates="resultados")
    examen: "Examen" = Relationship(back_populates="resultados")
    detalles: List["RespuestaDetalle"] = Relationship(
        back_populates="resultado",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
