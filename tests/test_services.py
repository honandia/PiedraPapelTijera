# tests/test_services.py

import pytest
from unittest.mock import MagicMock
from app.services import JuegoService
from app.models import Jugador, Partida, JugadaEnum

@pytest.fixture
def setup_service():
    partida_repo = MagicMock()
    jugador_repo = MagicMock()
    servicio = JuegoService(partida_repo, jugador_repo)
    return servicio, partida_repo, jugador_repo

def test_iniciar_partida(setup_service):
    servicio, partida_repo, _ = setup_service
    jugador1 = Jugador(nombre="Jugador1", tipo="humano")
    jugador2 = Jugador(nombre="Máquina", tipo="maquina")

    partida = servicio.iniciar_partida(jugador1, jugador2)
    
    partida_repo.save.assert_called_once()
    assert partida.estado == 'en curso'

def test_registrar_jugada_ganada(setup_service):
    servicio, partida_repo, _ = setup_service
    partida = Partida(id=1, estado='en curso')
    jugador = Jugador(id=1, nombre="Jugador1", tipo="humano")
    
    resultado = servicio.registrar_jugada(partida, jugador, JugadaEnum.PIEDRA, JugadaEnum.TIJERA)
    
    partida_repo.save.assert_called_once()
    assert resultado == 'ganada'

def test_registrar_jugada_perdida(setup_service):
    servicio, partida_repo, _ = setup_service
    partida = Partida(id=1, estado='en curso')
    jugador = Jugador(id=1, nombre="Jugador1", tipo="humano")

    resultado = servicio.registrar_jugada(partida, jugador, JugadaEnum.PIEDRA, JugadaEnum.PAPEL)
    
    partida_repo.save.assert_called_once()
    assert resultado == 'perdida'

def test_finalizar_partida(setup_service):
    servicio, partida_repo, jugador_repo = setup_service
    partida = Partida(id=1, estado='en curso', ganador_id=None)
    jugador = Jugador(id=1, nombre="Jugador1", tipo="humano", puntos=0)

    servicio.finalizar_partida(partida, jugador)

    partida_repo.save.assert_called_once()
    assert partida.estado == 'finalizada'
    assert jugador.puntos == 1
