from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from src.models.entity.user import User


class Emotions(SQLModel, table=True):
    __tablename__ = "emotions"
    id_usuario: int = Field(foreign_key="users.id")
    id: int| None = Field(default=None, primary_key=True)
    dominant_emotions: str | None = Field(default=None)
    angry: float | None = Field(default=None)
    disgust: float | None = Field(default=None)
    fear: float | None = Field(default=None)
    happy: float | None = Field(default=None)
    neutral: float | None = Field(default=None)
    sad: float | None = Field(default=None)
    surprise: float | None = Field(default=None)
    user: Optional[User] = Relationship(back_populates="emotions")