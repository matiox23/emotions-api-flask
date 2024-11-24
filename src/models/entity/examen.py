from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, func
from datetime import datetime
from src.models.entity.pregunta import Pregunta
from src.models.entity.resultado import Resultado

class Examen(SQLModel, table=True):
    __tablename__ = "examenes"
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(nullable=False)
    descripcion: Optional[str] = Field(default=None)
    fecha_creacion: datetime = Field(
        sa_column=Column("fecha_creacion", DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    preguntas: List[Pregunta] = Relationship(back_populates="examen", cascade_delete= "all, delete-orphan")
    resultados: List[Resultado] = Relationship(back_populates="examen", cascade_delete= "all, delete-orphan")
