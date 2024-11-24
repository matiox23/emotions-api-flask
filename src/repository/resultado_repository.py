from typing import List
from sqlmodel import Session, select
from src.db.database import engine
from src.models.entity.resultado import Resultado

class ResultadoRepository:
    @staticmethod
    def get_resultados_by_examen_id(examen_id: int) -> List[Resultado]:
        """Obtiene los resultados de un examen por su ID."""
        with Session(engine) as session:
            statement = select(Resultado).where(Resultado.examen_id == examen_id)
            resultados = session.exec(statement).all()
        return resultados

    @staticmethod
    def get_all_resultados() -> List[Resultado]:
        """Obtiene todos los resultados registrados."""
        with Session(engine) as session:
            resultados = session.exec(select(Resultado)).all()
        return resultados

    @staticmethod
    def save_resultado(resultado: Resultado) -> Resultado:
        """Guarda un resultado en la base de datos."""
        with Session(engine) as session:
            session.add(resultado)
            session.commit()
            session.refresh(resultado)
        return resultado
