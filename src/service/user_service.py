from venv import create
import cv2
import base64
import numpy as np
from deepface import DeepFace
from typing import List
from flask import abort
from werkzeug.security import check_password_hash, generate_password_hash

from src.models.dto.password_change_request import PasswordChangeRequest
from src.models.entity import user
from src.repository.user_repository import UserRepository
from src.models.entity.user import User
from src.models.dto.user_resquest import UserRequest
from src.models.dto.user_response import UserResponse


class UserService:

    def __init__(self,user_repository: UserRepository):
        self.user_repository = user_repository


    def get_by_id(self, user_id) -> UserResponse:
        """Obtiene un usuario por su ID y lo convierte a UserResponse"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            abort(404, f'El usuario con id: {user_id} no existe')

        return UserResponse(
            id=user.id,
            tipo_usuario=user.tipo_usuario,
            correo=user.correo,
            nombre=user.nombre,
            apellido=user.apellido,
            sexo=user.sexo,
            fecha_registro=user.fecha_registro
        )



    def get_all_users(self) -> List[UserResponse]:
        users = self.user_repository.get_all()
        return [
            UserResponse(
                id = user.id,
                tipo_usuario = user.tipo_usuario,
                correo = user.correo,
                nombre = user.nombre,
                apellido = user.apellido,
                sexo = user.sexo,
                fecha_registro = user.fecha_registro

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
            nombre=userRequest.nombre,
            apellido=userRequest.apellido,
            sexo=userRequest.sexo,

        )
        created_user = self.user_repository.add(new_user)
        return UserResponse(
            id = created_user.id,
            tipo_usuario= created_user.tipo_usuario,
            correo= created_user.correo,
            nombre= created_user.nombre,
            apellido= created_user.apellido,
            sexo= created_user.sexo,
            fecha_registro= created_user.fecha_registro

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

    def change_password(self, password_change_request: PasswordChangeRequest) -> None:
        user = self.user_repository.get_by_correo(password_change_request.correo)

        # Verificar la contraseña actual
        if  password_change_request.new_password == user.password:
            abort(400, "La nueva contraseña no puede ser igual a la actual")

        elif password_change_request.old_password != user.password:
            abort(400, "La contraseña antigua no coincide")

        # Guardar los cambios en el repositorio
        else:
            # Encriptar y actualizar con la nueva contraseña
            hashed_new_password = generate_password_hash(password_change_request.new_password)
            user.password = hashed_new_password
            user.password = password_change_request.new_password
            self.user_repository.update(user)

        # Obtener el usuario por correo
        if not user:
            abort(404, f"Usuario con correo {password_change_request.correo} no encontrado")


    def get_all_students(self) -> List[UserResponse]:
        students = self.user_repository.get_all_students()

        return  [
            UserResponse(
                id=student.id,
                tipo_usuario=student.tipo_usuario,
                correo=student.correo,
                nombre=student.nombre,
                apellido = student.apellido,
                sexo= student.sexo,
                fecha_registro=student.fecha_registro
            )
            for student in students
        ]















