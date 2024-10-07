# tests/test_models.py

import pytest
from app.schemas import JugadorBase, JugadaBase, PartidaBase
from app.models import JugadaEnum, TipoJugadorEnum

def test_jugador_base():
    jugador = JugadorBase(nombre="Jugador1", tipo=TipoJugadorEnum.HUMANO)
    assert jugador.nombre == "Jugador1"
    assert jugador.tipo == TipoJugadorEnum.HUMANO

def test_jugada_base():
    jugada = JugadaBase(tipo=JugadaEnum.PIEDRA, resultado="ganada")
    assert jugada.tipo == JugadaEnum.PIEDRA
    assert jugada.resultado == "ganada"

def test_partida_base():
    partida = PartidaBase(estado='en curso')
    assert partida.estado == 'en curso'
    assert partida.ganador is None
