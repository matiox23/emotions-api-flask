# src/repository/resultados_repository.py
from typing import List
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from src.db.database import engine
from src.models.entity.resultado import Resultado

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
