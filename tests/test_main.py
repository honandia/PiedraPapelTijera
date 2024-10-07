import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.repositories import PartidaRepository, JugadorRepository

# Simula una sesión de base de datos
@pytest.fixture
def mock_db_session():
    db_session = MagicMock()
    return db_session

# Configura el cliente de pruebas para FastAPI
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

# Prueba para el endpoint /get_global_info
def test_get_global_info(client, mock_db_session, monkeypatch):
    mock_partida_repo = MagicMock()
    mock_partida_repo.obtener_info_global.return_value = {
        "total_victorias": 10,
        "total_derrotas": 5,
        "total_partidas": 15,
        "winrate": 0.6666666666666666
    }

    monkeypatch.setattr(PartidaRepository, 'obtener_info_global', mock_partida_repo.obtener_info_global)
    
    response = client.get("/get_global_info")
    
    assert response.status_code == 200
    assert response.json() == {
        "total_victorias": 10,
        "total_derrotas": 5,
        "total_partidas": 15,
        "winrate": 0.6666666666666666
    }

# Prueba para el endpoint /mano_fuerte
def test_mano_fuerte(client, mock_db_session, monkeypatch):
    mock_partida_repo = MagicMock()
    mock_partida_repo.obtener_mano_fuerte.return_value = ("piedra", 60.0)

    monkeypatch.setattr(PartidaRepository, 'obtener_mano_fuerte', mock_partida_repo.obtener_mano_fuerte)
    
    response = client.get("/mano_fuerte")
    
    assert response.status_code == 200
    assert response.json() == {
        "mano_fuerte": "piedra",
        "porcentaje_victorias": 60.0
    }

# Prueba para el endpoint /mano_debil
def test_mano_debil(client, mock_db_session, monkeypatch):
    mock_partida_repo = MagicMock()
    mock_partida_repo.obtener_mano_debil.return_value = ("tijera", 40.0)

    monkeypatch.setattr(PartidaRepository, 'obtener_mano_debil', mock_partida_repo.obtener_mano_debil)
    
    response = client.get("/mano_debil")
    
    assert response.status_code == 200
    assert response.json() == {
        "mano_debil": "tijera",
        "porcentaje_derrotas": 40.0
    }

# Prueba para el endpoint /ranking
def test_ranking(client, mock_db_session, monkeypatch):
    mock_jugador_repo = MagicMock()
    mock_jugador_repo.obtener_ranking.return_value = [
        {"id": 1, "jugador": "Alice", "puntos": 100},
        {"id": 2, "jugador": "Bob", "puntos": 90},
        {"id": 3, "jugador": "Charlie", "puntos": 80},
    ]

    monkeypatch.setattr(JugadorRepository, 'obtener_ranking', mock_jugador_repo.obtener_ranking)
    
    response = client.get("/ranking")
    
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "jugador": "Alice", "puntos": 100},
        {"id": 2, "jugador": "Bob", "puntos": 90},
        {"id": 3, "jugador": "Charlie", "puntos": 80}
    ]

# Prueba para el endpoint /estadisticas
def test_estadisticas(client, mock_db_session, monkeypatch):
    mock_partida_repo = MagicMock()
    mock_partida_repo.obtener_estadisticas_partidas.return_value = {
        "total_partidas": 50,
        "partidas_ganadas": 30,
        "partidas_abandonadas": 5
    }

    monkeypatch.setattr(PartidaRepository, 'obtener_estadisticas_partidas', mock_partida_repo.obtener_estadisticas_partidas)
    
    response = client.get("/estadisticas")
    
    assert response.status_code == 200
    assert response.json() == {
        "total_partidas": 50,
        "partidas_ganadas": 30,
        "partidas_abandonadas": 5
    }
