from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    tipo_usuario: str = Field(nullable=False)
    correo: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    nombre: str = Field(nullable=False)
    profesor: "Profesor" = Relationship(back_populates="user")
    alumno: "Alumno" = Relationship(back_populates="user")
