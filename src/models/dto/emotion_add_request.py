from pydantic.v1 import BaseModel
from typing import Dict

class EmotionAddRequest(BaseModel):
    dominant_emotions: str
    angry: float
    disgust: float
    fear: float
    happy: float
    neutral: float
    sad: float
    surprise: float

