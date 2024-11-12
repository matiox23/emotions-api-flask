# src/models/dto/emotion_add_request.py

from pydantic.v1 import BaseModel

class EmotionAddRequest(BaseModel):
    id_usuario: int
    dominant_emotions: str
    angry: float
    disgust: float
    fear: float
    happy: float
    neutral: float
    sad: float
    surprise: float
