from typing import List

from sqlalchemy.orm import joinedload
from sqlmodel import Session, select
from src.db.database import engine
from src.models.entity.examen import Examen
from src.models.entity.pregunta import Pregunta

from src.models.entity.resultado import Resultado


class ExamenRepository:
    @staticmethod
    def get_all() -> list[Examen]:
        with Session(engine) as session:
            # Carga los datos relacionados usando `joinedload` correctamente
            query = (
                select(Examen)
                .options(
                    joinedload(Examen.preguntas).joinedload(Pregunta.opciones_respuesta)
                )
            )
            # Ejecuta la consulta y elimina duplicados con `unique()`
            result = session.exec(query).unique()
            return result.all()

    @staticmethod
    def add(entity):
        """
        Guarda una entidad en la base de datos y la devuelve actualizada con su ID generado.
        """
        with Session(engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)  # Refresca la entidad para obtener su ID
        return entity

    @staticmethod
    def update(examen: Examen) -> Examen:
        with Session(engine) as session:
            session.add(examen)
            session.commit()
            session.refresh(examen)
        return examen

    @staticmethod
    def delete(examen_id: int) -> bool:
        """Elimina un examen por su ID. Retorna True si se elimina, False si no existe."""
        with Session(engine) as session:
            examen = session.get(Examen, examen_id)
            if examen:
                session.delete(examen)
                session.commit()
                return True
            return False


    @staticmethod
    def get_by_id(examen_id: int) -> Examen | None:
        with Session(engine) as session:
            query = (
                select(Examen)
                .options(
                    joinedload(Examen.preguntas).joinedload(Pregunta.opciones_respuesta),  # Usar atributos de clase
                    joinedload(Examen.resultados)  # Carga los resultados relacionados
                )
                .where(Examen.id == examen_id)
            )
            examen = session.exec(query).first()
            return examen

    """
 
    @staticmethod
    def get_all_resultados():
        with Session(engine) as session:
            resultados = session.exec(select(Resultado)).all()
        return resultados
    """

    @staticmethod
    def get_resultados_by_examen(examen_id: int) -> List[Resultado]:
        """
        Recupera todos los resultados asociados a un examen específico.
        """
        with Session(engine) as session:
            query = (
                select(Resultado)
                .where(Resultado.examen_id == examen_id)
                .options(
                    joinedload(Resultado.examen).joinedload(Examen.preguntas),
                    joinedload(Resultado.examen).joinedload(Examen.resultados),
                )
            )
            resultados = session.exec(query).all()
        return resultados

    @staticmethod
    def add1(resultado: Resultado) -> Resultado:
        with Session(engine) as session:
            session.add(resultado)
            session.commit()
            session.refresh(resultado)
            print("Resultado guardado:", resultado)
        return resultado

    @staticmethod
    def get_all_result(self) -> List[Resultado]:
        with Session(engine) as session:
            resultados = session.exec(select(Resultado)).all()
            return resultados



