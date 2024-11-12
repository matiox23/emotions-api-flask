import base64
import numpy as np
import cv2
from deepface import DeepFace
from src.models.entity.emotions import Emotions
from src.repository.emotion_repository import EmotionRepository

class EmotionService:

    def __init__(self, emotion_repository: EmotionRepository):
        self.emotion_repository = emotion_repository

    def analyze_emotion(self, base64_image: str):
        # Quitar el prefijo 'data:image/jpeg;base64,' si existe
        if base64_image.startswith("data:image"):
            base64_image = base64_image.split(",")[1]

        try:
            # Decodificar la imagen base64
            img_data = base64.b64decode(base64_image)
            nparr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            raise ValueError("Error al decodificar la imagen: " + str(e))

        # Verificar si la imagen se cargó correctamente
        if img is None:
            raise ValueError("La imagen no se pudo decodificar correctamente")

        # Analizar la emoción con DeepFace
        try:
            result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        except Exception as e:
            raise ValueError("Error al analizar la emoción: " + str(e))

        # Asegurarse de que el resultado no esté vacío
        if not result:
            raise ValueError("No se pudo analizar la emoción")

        # Extraer el primer resultado
        deepface_result = result[0]
        emotion_scores = deepface_result['emotion']
        dominant_emotion = deepface_result['dominant_emotion']

        return emotion_scores, dominant_emotion

    def map_emotions_to_model(self, id_usuario: int, emotion_scores: dict, dominant_emotion: str):
        emotions = Emotions(
            id_usuario=id_usuario,
            dominant_emotions=dominant_emotion,
            angry=emotion_scores.get('angry'),
            disgust=emotion_scores.get('disgust'),
            fear=emotion_scores.get('fear'),
            happy=emotion_scores.get('happy'),
            neutral=emotion_scores.get('neutral'),
            sad=emotion_scores.get('sad'),
            surprise=emotion_scores.get('surprise')
        )
        return emotions

    def analyze_and_store_emotion(self, base64_image: str, user_id: int):
        # Analizar la emoción
        emotion_scores, dominant_emotion = self.analyze_emotion(base64_image)

        # Mapear los datos al modelo Emotions
        emotions = self.map_emotions_to_model(user_id, emotion_scores, dominant_emotion)

        # Guardar la instancia en la base de datos
        saved_emotion = self.emotion_repository.add(emotions)

        return saved_emotion

    def get_all_emotions(self):
        # Obtener todas las emociones del repositorio
        emotions = self.emotion_repository.get_all()
        return emotions
