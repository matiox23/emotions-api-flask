from sqlmodel import SQLModel, Field

class Emotions(SQLModel, table=True):
    __tablename__ = "emotions"
    id: int| None = Field(default=None, primary_key=True)
    dominant_emotions: str | None = Field(default=None)
    angry: float | None = Field(default=None)
    disgust: float | None = Field(default=None)
    fear: float | None = Field(default=None)
    happy: float | None = Field(default=None)
    neutral: float | None = Field(default=None)
    sad: float | None = Field(default=None)
    surprise: float | None = Field(default=None)