from http import HTTPStatus
from flask import abort, jsonify, request, Blueprint
from spectree import Response
from pydantic import ValidationError
from werkzeug.exceptions import Unauthorized

from src.models.dto.message_response import MessageResponse
from src.repository.auth_repository import AuthRepository
from src.service.auth_service import AuthService
from src.models.dto.auth_request import AuthRequest
from src.models.dto.auth_response import AuthResponse
from src.specification import spec

auth_router = Blueprint('auth_router', __name__)

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)

@auth_router.route('/auth/login', methods=['POST'])
@spec.validate(
    json=AuthRequest,
    resp=Response(
        HTTP_200=AuthResponse,
        HTTP_400=MessageResponse,
        HTTP_401=MessageResponse
    ),
    tags=['auth']
)
def login():
    try:
        data = request.get_json()
        auth_request = AuthRequest.parse_obj(data)
        auth_response = auth_service.login(auth_request)
        return jsonify(auth_response.dict()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
    except Unauthorized as e:
        return jsonify({'message': e.description}), HTTPStatus.UNAUTHORIZED
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(e))
