from typing import Optional
from flask import abort
from src.repository.auth_repository import AuthRepository
from src.models.dto.auth_request import AuthRequest
from src.models.dto.auth_response import AuthResponse

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def login(self, auth_request: AuthRequest) -> AuthResponse:
        user = self.auth_repository.login(
            correo=auth_request.correo,
            password=auth_request.password,
            tipo_usuario=auth_request.tipo_usuario
        )
        if not user:
            abort(401, "Credenciales incorrectas o tipo de usuario no coincide")

        return AuthResponse(
            id=user.id,
            nombre=user.nombre,
            correo=user.correo,
            tipo_usuario=user.tipo_usuario
        )
