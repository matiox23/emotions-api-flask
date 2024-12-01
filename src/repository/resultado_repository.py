# src/repository/resultados_repository.py
from cgitb import text
from typing import List
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from src.db.database import engine
from src.models.entity.examen import Examen
from src.models.entity.resultado import Resultado
from src.models.entity.user import User


class ResultadoRepository:
    def get_resultados_by_examen_id(self, examen_id: int) -> List[Resultado]:
        """Obtiene los resultados de un examen por su ID."""
        with Session(engine) as session:
            resultados = session.exec(
                select(Resultado)
                .where(Resultado.examen_id == examen_id)
                .options(selectinload(Resultado.detalles))
            ).all()
        return resultados

    def get_all_resultados(self) -> List[Resultado]:
        """Obtiene todos los resultados registrados."""
        with Session(engine) as session:
            resultados = session.exec(
                select(Resultado)
                .options(selectinload(Resultado.detalles))
            ).all()
        return resultados

    def save_resultado(self, resultado: Resultado) -> Resultado:
        """Guarda un resultado en la base de datos y carga las relaciones necesarias."""
        with Session(engine) as session:
            session.add(resultado)
            session.commit()
            session.refresh(resultado)
            # Cargar detalles usando selectinload
            resultado = session.exec(
                select(Resultado)
                .where(Resultado.id == resultado.id)
                .options(selectinload(Resultado.detalles))
            ).first()
        return resultado


    def obtener_resultados_con_usuarios(self):
            """Obtiene los resultados con los usuarios y el nombre del examen."""
            try:
                with Session(engine) as session:
                    # Realiza el INNER JOIN entre resultados, usuarios y examenes
                    query = session.query(
                        Resultado.id.label('resultado_id'),
                        Resultado.examen_id,
                        Resultado.puntaje,
                        Resultado.fecha,
                        User.id.label('usuario_id'),
                        User.nombre,
                        User.apellido,
                        User.correo,
                        Examen.titulo.label('examen_nombre')
                    ).join(
                        User, Resultado.usuario_id == User.id
                    ).join(
                        Examen, Resultado.examen_id == Examen.id
                    ).all()  # Devuelve una lista de tuplas

                return query  # La consulta retorna una lista de tuplas
            except Exception as e:
                raise Exception(f"Error al obtener resultados con usuarios: {str(e)}")


    def get_resultados_by_usuario_id(self, usuario_id: int):
        """Obtiene los resultados filtrados por el ID del usuario junto con el nombre del usuario."""
        with Session(engine) as session:
            resultados = session.query(
                Resultado.id.label('resultado_id'),
                Resultado.examen_id,
                Resultado.puntaje,
                Resultado.fecha,
                Examen.titulo.label('examen_nombre'),
                User.nombre.label('usuario_nombre'),
                User.apellido.label('usuario_apellido')
            ).join(
                Examen, Resultado.examen_id == Examen.id
            ).join(
                User, Resultado.usuario_id == User.id
            ).filter(Resultado.usuario_id == usuario_id).all()

        return resultados


