from typing import List
from datetime import datetime
from flask import abort

from src.models.dto.crear_examen_dto import CrearExamenDTO
from src.models.dto.examen_response_dto import ExamenResponseDTO
from src.models.dto.PreguntaResponseDTO import PreguntaResponseDTO
from src.models.dto.OpcionRespuestaResponseDTO import OpcionRespuestaResponseDTO
from src.models.dto.examen_resut_response import ResultadoExamenResponseDTO
from src.models.dto.resultado_request import ResultadoRequest
from src.models.dto.resultado_request import ResultadoRequest
from src.models.dto.resultado_response import ResultadoResponseDTO, RespuestaDetalleDTO
from src.models.entity.examen import Examen
from src.models.entity.pregunta import Pregunta
from src.models.entity.opcion_respuesta import OpcionRespuesta
from src.models.entity.resultado import Resultado
from src.repository.examen_repository import ExamenRepository
from src.repository.resultado_repository import ResultadoRepository


class ExamenService:
    def __init__(self, examen_repository: ExamenRepository):
        self.repository = examen_repository

    def get_all_examenes(self) -> List[ExamenResponseDTO]:
        """Obtiene todos los exámenes existentes junto con sus preguntas y opciones de respuesta."""
        examenes = self.repository.get_all()
        return [
            ExamenResponseDTO(
                id=examen.id,
                titulo=examen.titulo,
                descripcion=examen.descripcion,
                fecha_creacion=examen.fecha_creacion.isoformat() if examen.fecha_creacion else None,
                preguntas=[
                    PreguntaResponseDTO(
                        id=pregunta.id,
                        texto=pregunta.texto,
                        opciones_respuesta=[
                            OpcionRespuestaResponseDTO(
                                id=opcion.id,
                                texto=opcion.texto,
                                es_correcta=opcion.es_correcta
                            )
                            for opcion in pregunta.opciones_respuesta
                        ]
                    )
                    for pregunta in examen.preguntas
                ]
            )
            for examen in examenes
        ]

    def create_examen(self, examen_dto: CrearExamenDTO) -> ExamenResponseDTO:
        """Crea un nuevo examen con preguntas y opciones de respuesta."""

        # Crear examen y guardarlo
        nuevo_examen = Examen(
            titulo=examen_dto.titulo,
            descripcion=examen_dto.descripcion,
            fecha_creacion=datetime.utcnow()
        )
        nuevo_examen = self.repository.add(nuevo_examen)  # Guarda el examen

        # Verifica que el ID del examen se generó correctamente
        if not nuevo_examen.id:
            raise ValueError("El ID del examen no se generó correctamente en la base de datos.")

        # Crear preguntas asociadas y sus opciones de respuesta
        preguntas_response = []
        for pregunta_dto in examen_dto.preguntas:
            # Asocia la pregunta al examen
            nueva_pregunta = Pregunta(
                texto=pregunta_dto.texto,
                examen_id=nuevo_examen.id  # Usa el ID generado
            )
            nueva_pregunta = self.repository.add(nueva_pregunta)  # Guarda la pregunta

            # Crear opciones de respuesta asociadas
            opciones_response = []
            for opcion_dto in pregunta_dto.opciones_respuesta:
                nueva_opcion = OpcionRespuesta(
                    texto=opcion_dto.texto,
                    es_correcta=opcion_dto.es_correcta,
                    pregunta_id=nueva_pregunta.id  # Asocia la opción a la pregunta
                )
                nueva_opcion = self.repository.add(nueva_opcion)
                opciones_response.append(
                    OpcionRespuestaResponseDTO(
                        id=nueva_opcion.id,
                        texto=nueva_opcion.texto,
                        es_correcta=nueva_opcion.es_correcta
                    )
                )

            # Agrega la pregunta y sus opciones a la respuesta
            preguntas_response.append(
                PreguntaResponseDTO(
                    id=nueva_pregunta.id,
                    texto=nueva_pregunta.texto,
                    opciones_respuesta=opciones_response
                )
            )

        # Retornar la respuesta completa del examen creado
        return ExamenResponseDTO(
            id=nuevo_examen.id,
            titulo=nuevo_examen.titulo,
            descripcion=nuevo_examen.descripcion,
            fecha_creacion=nuevo_examen.fecha_creacion.isoformat(),
            preguntas=preguntas_response
        )

    def update_examen(self, examen_id: int, examen_dto: CrearExamenDTO) -> ExamenResponseDTO:
        """Actualiza un examen existente."""
        # Obtener el examen por ID
        examen = self.repository.get_by_id(examen_id)
        if not examen:
            abort(404, f"El examen con id: {examen_id} no existe")

        # Actualizar campos principales del examen
        examen.titulo = examen_dto.titulo
        examen.descripcion = examen_dto.descripcion

        # Manejar preguntas
        existing_questions = {pregunta.id: pregunta for pregunta in examen.preguntas}
        updated_questions = []

        for pregunta_dto in examen_dto.preguntas:
            if pregunta_dto.id and pregunta_dto.id in existing_questions:
                # Actualizar pregunta existente
                pregunta = existing_questions[pregunta_dto.id]
                pregunta.texto = pregunta_dto.texto

                # Manejar opciones de respuesta
                existing_options = {opcion.id: opcion for opcion in pregunta.opciones_respuesta}
                updated_options = []

                for opcion_dto in pregunta_dto.opciones_respuesta:
                    if opcion_dto.id and opcion_dto.id in existing_options:
                        # Actualizar opción existente
                        opcion = existing_options[opcion_dto.id]
                        opcion.texto = opcion_dto.texto
                        opcion.es_correcta = opcion_dto.es_correcta
                    else:
                        # Crear nueva opción
                        opcion = OpcionRespuesta(
                            texto=opcion_dto.texto,
                            es_correcta=opcion_dto.es_correcta
                        )
                    updated_options.append(opcion)

                pregunta.opciones_respuesta = updated_options
            else:
                # Crear nueva pregunta
                pregunta = Pregunta(
                    texto=pregunta_dto.texto,
                    opciones_respuesta=[
                        OpcionRespuesta(
                            texto=opcion.texto,
                            es_correcta=opcion.es_correcta
                        )
                        for opcion in pregunta_dto.opciones_respuesta
                    ]
                )
            updated_questions.append(pregunta)

        # Asignar las preguntas actualizadas al examen
        examen.preguntas = updated_questions

        # Actualizar el examen en el repositorio
        updated_examen = self.repository.update(examen)

        # Construir y retornar la respuesta del examen actualizado
        return ExamenResponseDTO(
            id=updated_examen.id,
            titulo=updated_examen.titulo,
            descripcion=updated_examen.descripcion,
            fecha_creacion=updated_examen.fecha_creacion.isoformat(),
            preguntas=[
                PreguntaResponseDTO(
                    id=pregunta.id,
                    texto=pregunta.texto,
                    opciones_respuesta=[
                        OpcionRespuestaResponseDTO(
                            id=opcion.id,
                            texto=opcion.texto,
                            es_correcta=opcion.es_correcta
                        )
                        for opcion in pregunta.opciones_respuesta
                    ]
                )
                for pregunta in updated_examen.preguntas
            ]
        )

    def delete_examen(self, examen_id: int) -> None:
        """
              Elimina un examen por su ID.
              Si no se encuentra el examen, lanza un error.
              """
        if not self.repository.delete(examen_id):
            abort(404, f"Examen con id: {examen_id} no encontrado")

    def registrar_resultado(self, examen_id: int, resultado_dto: ResultadoRequest) -> ResultadoResponseDTO:
        # Cambiar self.examen_repository por self.repository
        examen = self.repository.get_by_id(examen_id)
        if not examen:
            raise ValueError(f"Examen con ID {examen_id} no encontrado.")

        correctas = 0
        detalles = []

        for respuesta in resultado_dto.respuestas:
            # Buscar la pregunta correspondiente
            pregunta = next((p for p in examen.preguntas if p.id == respuesta.pregunta_id), None)
            if not pregunta:
                continue

            # Buscar la opción correcta
            opcion_correcta = next((o for o in pregunta.opciones_respuesta if o.es_correcta), None)
            if opcion_correcta and opcion_correcta.id == respuesta.opcion_id:
                correctas += 1
                detalles.append(RespuestaDetalleDTO(pregunta_id=pregunta.id, correcta=True))
            else:
                detalles.append(RespuestaDetalleDTO(pregunta_id=pregunta.id, correcta=False))

        # Calcular puntaje en base al número de respuestas correctas
        puntaje = (correctas / len(examen.preguntas)) * 100

        # Crear un nuevo registro de resultado
        nuevo_resultado = Resultado(
            usuario_id=resultado_dto.usuario_id,
            examen_id=examen_id,
            puntaje=int(puntaje),  # Convertir a entero
            fecha=datetime.utcnow()
        )

        # Guardar el resultado en la base de datos
        self.repository.add1(nuevo_resultado)

        # Devolver la respuesta
        return ResultadoResponseDTO(
            usuario_id=nuevo_resultado.usuario_id,
            examen_id=nuevo_resultado.examen_id,
            puntaje=nuevo_resultado.puntaje,
            detalles=detalles,
            fecha=nuevo_resultado.fecha
        )

    def obtener_todos_resultados(self) -> List[ResultadoExamenResponseDTO]:
        resultados = self.repository.get_all_result()
        resultados_dto = [
            ResultadoExamenResponseDTO(
                usuario_id=resultado.usuario_id,
                examen_id=resultado.examen_id,
                puntaje=resultado.puntaje,
                fecha=resultado.fecha  # El DTO formateará la fecha
            )
            for resultado in resultados
        ]
        return resultados_dto
