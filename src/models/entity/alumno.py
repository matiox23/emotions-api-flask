from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING



class Alumno(SQLModel, table=True):
    __tablename__ = "alumnos"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    apellidos: str = Field(nullable=False)

    user_id: int = Field(foreign_key="users.id", unique=True)
    user: Optional["User"] = Relationship(back_populates="alumno")