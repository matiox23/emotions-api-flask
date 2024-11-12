from http import HTTPStatus
from typing import List
from flask import jsonify, request, Blueprint
from spectree import Response
from pydantic import ValidationError

from src.models.dto.emotions_request import EmotionRequestDto
from src.models.dto.emotion_add_response import EmotionAddResponse
from src.repository.emotion_repository import EmotionRepository
from src.service.emotion_service import EmotionService
from src.specification import spec

emotions_router = Blueprint('emotions_router', __name__)

# Inicialización del servicio y repositorio de emociones
emotions_repository = EmotionRepository()
emotions_service = EmotionService(emotions_repository)

# Endpoint para obtener todas las emociones
@emotions_router.route('/emotions', methods=['GET'])
@spec.validate(resp=Response(HTTP_200=List[EmotionAddResponse]), tags=['emotions'])
def get_all_emotions():
    emotions = emotions_service.get_all_emotions()
    return jsonify([emotion.dict() for emotion in emotions]), HTTPStatus.OK

# Endpoint para analizar y almacenar emociones
@emotions_router.route('/emotions/analyze', methods=['POST'])
@spec.validate(json=EmotionRequestDto, resp=Response(HTTP_201=EmotionAddResponse), tags=['emotions'])
def analyze_and_store_emotion():
    try:
        # Obtener datos de la solicitud utilizando EmotionRequestDto
        data = request.get_json()
        emotion_request = EmotionRequestDto.parse_obj(data)

        # Llamar al servicio para analizar y almacenar emociones
        emotion_response = emotions_service.analyze_and_store_emotion(
            base64_image=emotion_request.img_base64,
            user_id=emotion_request.id_usuario
        )

        # Retornar la respuesta con el estado HTTP 201
        return jsonify(emotion_response.dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        # Aquí podrías agregar un registro del error
        return jsonify({"error": "Error interno del servidor"}), HTTPStatus.INTERNAL_SERVER_ERROR
