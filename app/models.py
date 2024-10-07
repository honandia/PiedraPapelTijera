from app.schemas import JugadaEnum, ResultadoJugadaEnum, EstadoPartidaEnum, TipoJugadorEnum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Jugador(Base):
    __tablename__ = 'jugadores'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String)
    tipo = Column(SqlEnum(TipoJugadorEnum)) # 'humano' o 'maquina'
    puntos = Column(Integer, default=0)

class Partida(Base):
    __tablename__ = 'partidas'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    estado = Column(SqlEnum(EstadoPartidaEnum), default=EstadoPartidaEnum.EN_CURSO)  # 'en curso', 'finalizada', 'abandonada'
    ganador_id = Column(Integer, ForeignKey('jugadores.id'))
    ganador = relationship("Jugador", foreign_keys=[ganador_id])

class Jugada(Base):
    __tablename__ = 'jugadas'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    partida_id = Column(Integer, ForeignKey('partidas.id'))
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    tipo = Column(SqlEnum(JugadaEnum)) # 'piedra', 'papel', 'tijera'
    resultado = Column(SqlEnum(ResultadoJugadaEnum))  # 'ganada', 'perdida', 'empate'
