# src/controller/resultados_controller.py

from http import HTTPStatus
from typing import List

from flask import Blueprint, jsonify, request
from spectree import Response
from werkzeug.exceptions import NotFound
from src.models.dto.resultado_request import ResultadoRequest
from src.models.dto.resultado_response import ResultadoResponseDTO
from src.models.dto.error_response import ErrorResponse
from src.repository.resultado_repository import ResultadoRepository
from src.repository.examen_repository import ExamenRepository
from src.service.resultado_service import ResultadoService
from src.specification import spec  # Asegúrate de tener configurado Spectree

resultado_router = Blueprint("resultado_router", __name__)

# Inicializar los repositorios
resultado_repository = ResultadoRepository()
examen_repository = ExamenRepository()

# Inicializar el servicio con ambos repositorios
resultado_service = ResultadoService(resultado_repository, examen_repository)


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


@resultado_router.route("/examenes/<int:examen_id>/resultados", methods=["POST"])
@spec.validate(
    json=ResultadoRequest,
    resp=Response(
        HTTP_201=ResultadoResponseDTO,
        HTTP_400=ErrorResponse
    ),
    tags=["resultados"]
)
def registrar_resultado(examen_id: int):
    """Registra un nuevo resultado para un examen."""
    try:
        data = request.get_json()
        resultado_request = ResultadoRequest.parse_obj(data)
        resultado_response = resultado_service.registrar_resultado(examen_id, resultado_request)
        return jsonify(resultado_response.dict()), HTTPStatus.CREATED
    except NotFound as e:
        return jsonify({"error": e.description}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


@resultado_router.route('/resultados/usuarios', methods=['GET'])
@spec.validate(
    tags=["resultados"],
)
def obtener_resultados_con_usuarios():
    """Devuelve los resultados junto con los detalles de los usuarios."""
    try:
        resultados_con_usuarios = resultado_service.obtener_resultados_con_usuarios()
        if not resultados_con_usuarios:
            return jsonify({"error": "No se encontraron resultados con los usuarios."}), HTTPStatus.NOT_FOUND
        return jsonify(resultados_con_usuarios), HTTPStatus.OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@resultado_router.route('/usuarios/<int:usuario_id>/resultados', methods=['GET'])
@spec.validate(
    tags=["resultados"],
)
def get_resultados_by_usuario_id(usuario_id: int):
    """Devuelve los resultados asociados a un usuario por su ID, incluyendo su nombre."""
    try:
        resultados = resultado_service.get_resultados_by_usuario_id(usuario_id)

        if not resultados:
            return jsonify({"message": "No se encontraron resultados para este usuario."}), HTTPStatus.NOT_FOUND

        return jsonify(resultados), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
