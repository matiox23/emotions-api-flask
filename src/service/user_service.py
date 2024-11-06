from venv import create
import cv2
import base64
import numpy as np
from deepface import DeepFace
from typing import List
from flask import abort
from src.repository.user_repository import UserRepository
from src.models.entity.user import User
from src.models.dto.user_resquest import UserRequest
from src.models.dto.user_response import UserResponse


class UserService:

    def __init__(self,user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self) -> List[UserResponse]:
        users = self.user_repository.get_all()
        return [
            UserResponse(
                id = user.id,
                tipo_usuario = user.tipo_usuario,
                correo = user.correo,
                nombre = user.nombre

            )
            for user in users
        ]

    def insert_user(self, userRequest: UserRequest) -> UserResponse:
        if self.user_repository.exists_by_correo(userRequest.correo):
            abort(409,f'Correo {userRequest.correo} ya existe')

        new_user = User(
            tipo_usuario=userRequest.tipo_usuario,
            correo=userRequest.correo,
            password=userRequest.password,
            nombre=userRequest.nombre
        )
        created_user = self.user_repository.add(new_user)
        return UserResponse(
            id = created_user.id,
            tipo_usuario= created_user.tipo_usuario,
            correo= created_user.correo,
            nombre= created_user.nombre
        )

    def update_user(self, user_id:int, user_request:UserRequest) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            abort(404,f'El usuario con id: {user_id} no existe ')

        user.nombre = user_request.nombre,
        user.correo = user_request.correo,
        user.password = user_request.password
        user.tipo_usuario = user_request.tipo_usuario

        user_update = self.user_repository.update(user)

        return UserResponse(
            id = user_update.id,
            tipo_usuario= user_update.tipo_usuario,
            nombre= user_update.nombre,
            correo= user_update.correo,

        )

    def delete_user(self, user_id:int) -> None:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            abort(404,f'El usuario con id: {user_id} no existe ')
        self.user_repository.delete(user_id)












