from venv import create
import cv2
import base64
import numpy as np
from deepface import DeepFace
from typing import List, Dict
from flask import abort

from src.models.dto.emotions_request import EmotionRequestDto
from src.models.dto.emotions_response import EmotionResponseDto
from src.repository.emotion_repository import EmotionRepository
from src.models.entity.emotions import Emotions
from src.models.dto.emotion_add_request import EmotionAddRequest
from src.models.dto.emotion_add_response import EmotionAddResponse


class EmotionService:

    def __init__(self,emotion_repository: EmotionRepository):
        self.emotion_repository = emotion_repository

    def get_all_emotions(self) -> List[EmotionAddResponse]:
        emotions = self.emotion_repository.get_all()
        return [
            EmotionAddResponse(
                id = emotion.id,
                dominant_emotions = emotion.dominant_emotions,
                angry = emotion.angry,
                disgust = emotion.disgust,
                fear = emotion.fear,
                happy = emotion.happy,
                neutral = emotion.neutral,
                sad = emotion.sad,
                surprise = emotion.surprise

            )
            for emotion in emotions
        ]

    def insert_emotion(self, emotion_add_request: EmotionAddRequest) -> EmotionAddResponse:
        new_emotions = Emotions(
            dominant_emotions= emotion_add_request.dominant_emotions,
            angry=emotion_add_request.angry,
            disgust=emotion_add_request.disgust,
            fear=emotion_add_request.fear,
            happy=emotion_add_request.happy,
            neutral=emotion_add_request.neutral,
            sad=emotion_add_request.sad,
            surprise=emotion_add_request.surprise
        )
        created_emotions = self.emotion_repository.add(new_emotions)
        return EmotionAddResponse(
            id = created_emotions.id,
            dominant_emotions = created_emotions.dominant_emotions,
            angry = created_emotions.angry,
            disgust = created_emotions.disgust,
            fear = created_emotions.fear,
            happy = created_emotions.happy,
            neutral = created_emotions.neutral,
            sad = created_emotions.sad,
            surprise = created_emotions.surprise
        )

    def analyze_emotion(base64_image: str):
        # Quitar el prefijo 'data:image/jpeg;base64,' si existe
        if base64_image.startswith("data:image"):
            base64_image = base64_image.split(",")[1]

        # Decodificar la imagen base64
        img_data = base64.b64decode(base64_image)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Verificar si la imagen se cargó correctamente
        if img is None:
            raise ValueError("La imagen no se pudo decodificar")

        # Analizar la emoción con DeepFace
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)

        return result










