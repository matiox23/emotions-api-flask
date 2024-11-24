from typing import List

from sqlmodel import SQLModel, Field, Relationship, DateTime, Column, func
from datetime  import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    tipo_usuario: str = Field(nullable=False)
    correo: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    nombre: str = Field(nullable=False)
    apellido: str = Field(nullable=False)
    sexo: str = Field(nullable=False)
    fecha_registro: datetime = Field(
        sa_column=Column("fecha_registro", DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    # Relaciones
    resultados: List["Resultado"] = Relationship(back_populates="user")

    profesor: "Profesor" = Relationship(back_populates="user")
    alumno: "Alumno" = Relationship(back_populates="user")
    emotions: List["Emotions"] = Relationship(back_populates="user")


