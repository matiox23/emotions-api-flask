from typing import List
from flask import abort,  jsonify, request, Blueprint
from spectree import Response
from pydantic.v1 import ValidationError

from src.models.dto.emotions_request import EmotionRequestDto
from src.models.dto.emotions_response import EmotionResponseDto
from src.models.dto.message_response import MessageResponse
from src.service.emotion_service import EmotionService
from src.repository.emotion_repository import EmotionRepository
from src.models.dto.emotion_add_request import EmotionAddRequest
from src.models.dto.emotion_add_response import EmotionAddResponse
from src.models.dto.error_message import ErrorResponseMessage
from src.specification import spec

emotions_router = Blueprint('emotions_router', __name__)

emotions_repository = EmotionRepository()
emotions_service = EmotionService(emotions_repository)

@emotions_router.route('/emotions', methods=['GET'])
@spec.validate(resp=Response(HTTP_200=List[EmotionAddResponse]),tags=['emotions'])
def get_all_emotions():
    emotions = emotions_service.get_all_emotions()
    return jsonify([emotion.dict() for emotion in emotions]), 200

@emotions_router.route('/emotions', methods=['POST'])
@spec.validate(json=EmotionAddRequest, resp=Response(HTTP_201=EmotionAddResponse), tags=['emotions'])
def create_priority():
    try:
        data = request.get_json()
        emotions_request = EmotionAddRequest.parse_obj(data)
        add_emotions = emotions_service.insert_emotion(emotions_request)
        emotions_reponse = EmotionAddResponse.from_orm(add_emotions)
        return jsonify(emotions_reponse.dict()), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        abort(400, description=str(e))


@emotions_router.route('/emotions/analyze', methods=['POST'])
@spec.validate(
    json=EmotionRequestDto,
    resp=Response(
        HTTP_200=EmotionResponseDto,
        HTTP_400=MessageResponse,
        HTTP_500=MessageResponse
    ),
    tags=['emotions']
)
def analyze_emotion():
    try:
        # Obtener los datos de la solicitud y validar el DTO
        data = request.get_json()
        dto = EmotionRequestDto(**data)

        # Llamar al servicio para procesar la emoción
        result = EmotionService.analyze_emotion(dto.img_base64)

        # Extraer solo las emociones y la emoción dominante
        emotions = result[0]['emotion']
        dominant_emotion = result[0]['dominant_emotion']

        # Crear el ResponseDto con los datos procesados
        response_dto = EmotionResponseDto(
            emotions=emotions,
            dominant_emotion=dominant_emotion
        )

        # Devolver la respuesta como JSON
        return jsonify(response_dto.dict()), 200

    except Exception as e:
        # Manejo de errores, devuelve una respuesta de error
        return jsonify({"error": str(e)}), 500