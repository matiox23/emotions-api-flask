from pydantic.v1 import BaseModel

class EmotionAddResponse(BaseModel):
    id: int
    dominant_emotions: str
    angry: float
    disgust: float
    fear: float
    happy: float
    neutral: float
    sad: float
    surprise: float

    class Config:
        orm_mode = True
