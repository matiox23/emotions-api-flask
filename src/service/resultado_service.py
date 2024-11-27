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
