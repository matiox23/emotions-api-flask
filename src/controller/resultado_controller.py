from http import HTTPStatus
from typing import List

from flask import Blueprint, jsonify, request
from spectree import Response
from werkzeug.exceptions import NotFound
from src.models.dto.resultado_request import ResultadoRequest
from src.models.dto.resultado_response import ResultadoResponseDTO
from src.models.dto.error_response import ErrorResponse
from src.repository.resultado_repository import ResultadoRepository
from src.service.resultado_service import ResultadoService
from src.specification import spec

resultado_router = Blueprint("resultado_router", __name__)

resultado_repository = ResultadoRepository()
resultado_service = ResultadoService(resultado_repository)

@resultado_router.route("/resultados", methods=["GET"])
@spec.validate(resp=Response(HTTP_200=List[ResultadoResponseDTO]), tags=["resultados"])
def get_all_resultados():
    """Devuelve todos los resultados."""
    try:
        resultados = resultado_service.get_all_resultados()
        return jsonify([resultado.dict() for resultado in resultados]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@resultado_router.route("/examenes/<int:examen_id>/resultados", methods=["GET"])
@spec.validate(resp=Response(HTTP_200=List[ResultadoResponseDTO]), tags=["resultados"])
def get_resultados_by_examen_id(examen_id: int):
    """Devuelve los resultados de un examen específico."""
    try:
        resultados = resultado_service.get_resultados_by_examen_id(examen_id)
        return jsonify([resultado.dict() for resultado in resultados]), HTTPStatus.OK
    except NotFound as e:
        return jsonify({"error": e.description}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@resultado_router.route("/resultados", methods=["POST"])
@spec.validate(json=ResultadoRequest, resp=Response(HTTP_201=ResultadoResponseDTO, HTTP_400=ErrorResponse), tags=["resultados"])
def save_resultado():
    """Guarda un nuevo resultado."""
    try:
        data = request.get_json()
        resultado_request = ResultadoRequest.parse_obj(data)
        resultado = resultado_service.save_resultado(
            usuario_id=resultado_request.usuario_id,
            examen_id=resultado_request.respuestas[0].pregunta_id,  # Ajusta según la lógica
            puntaje=100  # Esto debería calcularse según la lógica del examen
        )
        return jsonify(resultado.dict()), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
