from typing import List
from flask import abort
from src.models.dto.resultado_response import ResultadoResponseDTO, RespuestaDetalleDTO
from src.models.entity import pregunta
from src.repository.resultado_repository import ResultadoRepository
from src.models.entity.resultado import Resultado


class ResultadoService:
    def __init__(self, resultado_repository: ResultadoRepository):
        self.resultado_repository = resultado_repository

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
                detalles=[RespuestaDetalleDTO]  # Si hay más detalles, ajusta aquí
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

    def save_resultado(self, usuario_id: int, examen_id: int, puntaje: int) -> ResultadoResponseDTO:
        """Guarda un nuevo resultado y devuelve el DTO."""
        nuevo_resultado = Resultado(
            usuario_id=usuario_id,
            examen_id=examen_id,
            puntaje=puntaje,
        )
        resultado_guardado = self.resultado_repository.save_resultado(nuevo_resultado)
        return ResultadoResponseDTO(
            usuario_id=resultado_guardado.usuario_id,
            examen_id=resultado_guardado.examen_id,
            puntaje=resultado_guardado.puntaje,
            fecha=resultado_guardado.fecha.isoformat(),
            detalles=[]  # Si necesitas detalles, ajusta aquí
        )
