from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, func
from datetime import datetime

class Resultado(SQLModel, table=True):
    __tablename__ = "resultados"
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="users.id", nullable=False)
    examen_id: int = Field(foreign_key="examenes.id", nullable=False)
    puntaje: int = Field(nullable=False)
    fecha: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

    # Relaciones diferidas
    user: "User" = Relationship(back_populates="resultados")
    examen: "Examen" = Relationship(back_populates="resultados")
