import pytest

def test_get_all_resultados(client):
    """Prueba la ruta para obtener todos los resultados."""
    response = client.get("/resultados")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_resultados_by_usuario_id(client):
    """Prueba la ruta para obtener resultados por ID de usuario."""
    usuario_id = 1  # Ajusta según tus datos de prueba
    response = client.get(f"/usuarios/{usuario_id}/resultados")
    assert response.status_code == 200
    assert isinstance(response.json, list)
