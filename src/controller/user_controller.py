from http import HTTPStatus
from typing import List
from flask import abort,  jsonify, request, Blueprint
from spectree import Response
from pydantic.v1 import ValidationError
from werkzeug.exceptions import NotFound

from src.models.dto.message_response import MessageResponse
from src.models.dto.password_change_request import PasswordChangeRequest
from src.repository.user_repository import UserRepository
from src.service.user_service import UserService
from src.models.dto.user_response import UserResponse
from src.models.dto.user_resquest import UserRequest
from src.specification import spec

user_router = Blueprint('users_router', __name__)

user_repository = UserRepository()
user_service = UserService(user_repository)

@user_router.route('/users', methods=['GET'])
@spec.validate(resp=Response(HTTP_200=List[UserResponse]),tags=['users'])
def get_users():
    users = user_service.get_all_users()
    return jsonify([user.dict() for user in users]),200


#Crear usuario
@user_router.route('/users', methods=['POST'])
@spec.validate(json=UserRequest, resp=Response(HTTP_201=UserResponse), tags=['users'])
def create_priority():
    try:
        data = request.get_json()
        user_request = UserRequest.parse_obj(data)
        add_user = user_service.insert_user(user_request)
        user_reponse = UserResponse.from_orm(add_user)
        return jsonify(user_reponse.dict()), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        abort(400, description=str(e))

@user_router.route("/users/<int:id>", methods=["PUT"])
@spec.validate(json=UserRequest, resp=Response(HTTP_200=UserResponse), tags=['users'])
def update_users(id: int):
    try:
        data = request.get_json()
        user_request = UserRequest.parse_obj(data)
        updated_user = user_service.update_user(id, user_request)
        user_response = UserResponse.from_orm(updated_user)
        return jsonify(user_response.dict()), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except ValueError as e:
        abort(400, description=str(e))

@user_router.route('/users/<int:id>', methods=['DELETE'])
@spec.validate(
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_404=MessageResponse,
        HTTP_400=MessageResponse
    ),
    tags=['users']
)
def delete_user(id: int):
    try:
        user_service.delete_user(id)
        return jsonify({'message': 'Usuario eliminado'}), 200
    except NotFound as e:
        return jsonify({'message': e.description}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@user_router.route('/users/change-password', methods=['PUT'])
@spec.validate(json=PasswordChangeRequest, resp=Response(HTTP_200=MessageResponse, HTTP_400=MessageResponse), tags=['users'])
def change_password():
    try:
        data = request.get_json()
        password_change_request = PasswordChangeRequest.parse_obj(data)
        user_service.change_password(password_change_request)
        return jsonify({'message': 'Contraseña actualizada exitosamente'}), HTTPStatus.OK
    except NotFound as e:
        return  jsonify({'message': e.description}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@user_router.route('/users/students', methods=['GET'])
@spec.validate(resp=Response(HTTP_200=List[UserResponse]), tags=['users'])
def get_all_students():
    students = user_service.get_all_students()
    return jsonify([student.dict() for student in students]), 200
