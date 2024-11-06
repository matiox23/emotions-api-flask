# src/models/dto/emotion_response_dto.py

from pydantic.v1 import BaseModel
from typing import Dict

class EmotionResponseDto(BaseModel):
    emotions: Dict[str, float]
    dominant_emotion: str
