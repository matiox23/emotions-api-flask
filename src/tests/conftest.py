import pytest
from src.__main__ import app as flask_app  # Ajusta según tu estructura

@pytest.fixture
def app():
    """Proporciona la aplicación Flask para las pruebas."""
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Base de datos en memoria
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Proporciona el cliente de pruebas de Flask."""
    return app.test_client()
