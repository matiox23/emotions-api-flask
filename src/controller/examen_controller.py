from http import HTTPStatus
from typing import List

from flask import Blueprint, jsonify, request, abort
from spectree import Response
from pydantic.v1 import ValidationError
from werkzeug.exceptions import NotFound

from src.models.dto.crear_examen_dto import CrearExamenDTO
from src.models.dto.error_response import ErrorResponse
from src.models.dto.examen_response_dto import ExamenResponseDTO
from src.models.dto.examen_resut_response import ResultadoExamenResponseDTO
from src.models.dto.lista_examenes_response_dto import ListaExamenesResponseDTO
from src.models.dto.lista_resultado_response_dto import ListaResultadosResponseDTO
from src.models.dto.message_response import MessageResponse
from src.models.dto.resultado_request import ResultadoRequest
from src.service.examen_service import ExamenService
from src.models.dto.resultado_response import ResultadoResponseDTO, RespuestaDetalleDTO
from src.repository.examen_repository import ExamenRepository
from src.specification import spec

# Inicializar el blueprint y el servicio
examen_router = Blueprint('examen_router', __name__)
examen_service = ExamenService(ExamenRepository())

# Obtener todos los exámenes
@examen_router.route('/examenes', methods=['GET'])
@spec.validate(resp=Response(HTTP_200=ListaExamenesResponseDTO), tags=['examenes'])
def get_examenes():
    try:
        examenes = examen_service.get_all_examenes()
        response = ListaExamenesResponseDTO(examenes=examenes)
        return jsonify(response.dict()), HTTPStatus.OK
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))
# Crear un nuevo examen
@examen_router.route('/examenes', methods=['POST'])
@spec.validate(json=CrearExamenDTO, resp=Response(HTTP_201=ExamenResponseDTO), tags=['examenes'])
def create_examen():
    try:
        data = request.get_json()
        examen_dto = CrearExamenDTO.parse_obj(data)
        created_examen = examen_service.create_examen(examen_dto)
        return jsonify(created_examen.dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))

# Actualizar un examen existente
@examen_router.route('/examenes/<int:examen_id>', methods=['PUT'])
@spec.validate(json=CrearExamenDTO, resp=Response(HTTP_200=ExamenResponseDTO), tags=['examenes'])
def update_examen(examen_id: int):
    try:
        data = request.get_json()
        examen_dto = CrearExamenDTO.parse_obj(data)
        updated_examen = examen_service.update_examen(examen_id, examen_dto)
        return jsonify(updated_examen.dict()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
    except ValueError as e:
        abort(HTTPStatus.NOT_FOUND, description=str(e))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))

# Eliminar un examen
@examen_router.route('/examenes/<int:id>', methods=['DELETE'])
@spec.validate(
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_404=MessageResponse,
        HTTP_400=MessageResponse
    ),
    tags=['examenes']
)
def delete_examen(id: int):
    """
    Endpoint para eliminar un examen por su ID.
    Retorna 200 si se elimina exitosamente, 404 si no existe y 400 para errores generales.
    """
    try:
        examen_service.delete_examen(id)
        return jsonify({'message': 'Examen eliminado exitosamente'}), HTTPStatus.OK
    except NotFound as e:
        return jsonify({'message': e.description}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST



"""
@examen_router.route('/examenes/<int:examen_id>/resultados', methods=['POST'])
@spec.validate(
    json=ResultadoRequest,
    resp=Response(HTTP_201=ResultadoResponseDTO, HTTP_400=ErrorResponse),
    tags=["examenes"]
)
def registrar_resultado(examen_id: int):
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        resultado_dto = ResultadoRequest.parse_obj(data)

        # Registrar resultado a través del servicio
        resultado = examen_service.registrar_resultado(examen_id, resultado_dto)

        # Respuesta exitosa
        return jsonify(resultado.dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"error": "Error de validación"}), HTTPStatus.BAD_REQUEST
    except ValueError as e:
        abort(HTTPStatus.NOT_FOUND, description=str(e))
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))

"""










