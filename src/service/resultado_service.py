# src/service/resultados_service.py

from typing import List
from flask import abort
from datetime import datetime
from src.models.dto.resultado_request import ResultadoRequest, RespuestaDTO
from src.models.dto.resultado_response import ResultadoResponseDTO, RespuestaDetalleDTO
from src.models.entity.resultado import Resultado
from src.models.entity.respuesta_detalle import RespuestaDetalle
from src.repository.resultado_repository import ResultadoRepository
from src.repository.examen_repository import ExamenRepository


class ResultadoService:
    def __init__(self, resultado_repository: ResultadoRepository, examen_repository: ExamenRepository):
        self.resultado_repository = resultado_repository
        self.examen_repository = examen_repository

    def get_resultados_by_examen_id(self, examen_id: int) -> List[ResultadoResponseDTO]:
        """Obtiene resultados de un examen por ID y los transforma en DTOs."""
        resultados = self.resultado_repository.get_resultados_by_examen_id(examen_id)
        if not resultados:
            abort(404, f"No hay resultados registrados para el examen con ID {examen_id}.")

        return [
            ResultadoResponseDTO(
                usuario_id=resultado.usuario_id,
                examen_id=resultado.examen_id,
                puntaje=resultado.puntaje,
                fecha=resultado.fecha.isoformat(),
                detalles=[
                    RespuestaDetalleDTO(
                        pregunta_id=detalle.pregunta_id,
                        correcta=detalle.correcta
                    ) for detalle in resultado.detalles
                ]
            )
            for resultado in resultados
        ]

    def get_all_resultados(self) -> List[ResultadoResponseDTO]:
        """Obtiene todos los resultados y los transforma en DTOs."""
        resultados = self.resultado_repository.get_all_resultados()
        return [
            ResultadoResponseDTO(
                usuario_id=resultado.usuario_id,
                examen_id=resultado.examen_id,
                puntaje=resultado.puntaje,
                fecha=resultado.fecha.isoformat(),
                detalles=[
                    RespuestaDetalleDTO(
                        pregunta_id=detalle.pregunta_id,
                        correcta=detalle.correcta
                    ) for detalle in resultado.detalles
                ]
            )
            for resultado in resultados
        ]

    def registrar_resultado(self, examen_id: int, resultado_request: ResultadoRequest) -> ResultadoResponseDTO:
        """Registra un nuevo resultado basado en las respuestas proporcionadas."""
        examen = self.examen_repository.get_by_id(examen_id)
        if not examen:
            abort(404, f"Examen con ID {examen_id} no encontrado.")

        correctas = 0
        detalles_respuesta_detalle = []

        for respuesta in resultado_request.respuestas:
            pregunta = next((p for p in examen.preguntas if p.id == respuesta.pregunta_id), None)
            if not pregunta:
                abort(400, f"Pregunta con ID {respuesta.pregunta_id} no encontrada en el examen.")

            opcion_correcta = next((o for o in pregunta.opciones_respuesta if o.es_correcta), None)
            es_correcta = opcion_correcta and opcion_correcta.id == respuesta.opcion_id

            if es_correcta:
                correctas += 1

            detalle_respuesta = RespuestaDetalle(
                pregunta_id=pregunta.id,
                correcta=es_correcta
            )
            detalles_respuesta_detalle.append(detalle_respuesta)

        # Evita división por cero si no hay preguntas
        puntaje = (correctas / len(examen.preguntas)) * 100 if examen.preguntas else 0

        nuevo_resultado = Resultado(
            usuario_id=resultado_request.usuario_id,
            examen_id=examen_id,
            puntaje=int(puntaje),
            fecha=datetime.utcnow(),
            detalles=detalles_respuesta_detalle  # Asigna los detalles
        )

        # Guardar el resultado y obtener la instancia con detalles cargados
        resultado_guardado = self.resultado_repository.save_resultado(nuevo_resultado)

        # Convertir a DTO dentro del contexto de la sesión donde 'detalles' están cargados
        detalles_dto = [
            RespuestaDetalleDTO(
                pregunta_id=detalle.pregunta_id,
                correcta=detalle.correcta
            ) for detalle in resultado_guardado.detalles
        ]

        return ResultadoResponseDTO(
            usuario_id=resultado_guardado.usuario_id,
            examen_id=resultado_guardado.examen_id,
            puntaje=resultado_guardado.puntaje,
            fecha=resultado_guardado.fecha.isoformat(),
            detalles=detalles_dto
        )

    def obtener_resultados_con_usuarios(self):
        """Obtiene los resultados con los detalles de los usuarios y el nombre del examen."""
        try:
            resultados_con_usuarios = self.resultado_repository.obtener_resultados_con_usuarios()

            if not resultados_con_usuarios:
                return None

            # Mapea los resultados a un formato adecuado para la respuesta
            response_data = []
            for resultado in resultados_con_usuarios:
                response_data.append({
                    'resultado_id': resultado.resultado_id,
                    'examen_id': resultado.examen_id,
                    'puntaje': resultado.puntaje,
                    'fecha': resultado.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                    'usuario_id': resultado.usuario_id,
                    'nombre': resultado.nombre,
                    'apellido': resultado.apellido,
                    'correo': resultado.correo,
                    'examen_nombre': resultado.examen_nombre
                })

            return response_data
        except Exception as e:
            raise Exception(f"Error al obtener resultados con usuarios: {str(e)}")

    def get_resultados_by_usuario_id(self, usuario_id: int):
        """Obtiene los resultados por ID del usuario incluyendo su nombre."""
        resultados = self.resultado_repository.get_resultados_by_usuario_id(usuario_id)

        if not resultados:
            return []

        return [
            {
                "resultado_id": resultado.resultado_id,
                "examen_id": resultado.examen_id,
                "examen_nombre": resultado.examen_nombre,
                "usuario_nombre": resultado.usuario_nombre,
                "usuario_apellido": resultado.usuario_apellido,
                "puntaje": resultado.puntaje,
                "fecha": resultado.fecha.strftime('%Y-%m-%d %H:%M:%S')
            }
            for resultado in resultados
        ]
