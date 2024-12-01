import pytest
from src.service.resultado_service import ResultadoService
from src.repository.resultado_repository import ResultadoRepository
from src.repository.examen_repository import ExamenRepository

@pytest.fixture
def mock_repositories():
    resultado_repository = ResultadoRepository()
    examen_repository = ExamenRepository()
    return resultado_repository, examen_repository

def test_get_all_resultados(mock_repositories):
    """Prueba para obtener todos los resultados."""
    resultado_repository, examen_repository = mock_repositories
    service = ResultadoService(resultado_repository, examen_repository)

    resultados = service.get_all_resultados()
    assert isinstance(resultados, list)
