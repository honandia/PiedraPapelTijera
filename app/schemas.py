from pydantic import BaseModel
from enum import Enum

class JugadaEnum(str, Enum):
    PIEDRA = 'piedra'
    PAPEL = 'papel'
    TIJERA = 'tijera'

class TipoJugadorEnum(str, Enum):
    HUMANO = 'humano'
    MAQUINA = 'maquina'

class ResultadoJugadaEnum(str, Enum):
    GANADA = 'ganada'
    PERDIDA = 'perdida'
    EMPATE = 'empate'

class EstadoPartidaEnum(str, Enum):
    EN_CURSO = 'en curso'
    FINALIZADA = 'finalizada'
    ABANDONADA = 'abandonada'

class JugadorBase(BaseModel):
    nombre: str
    tipo: TipoJugadorEnum

class JugadaBase(BaseModel):
    tipo: JugadaEnum
    resultado: ResultadoJugadaEnum

class PartidaBase(BaseModel):
    estado: str
    ganador: JugadorBase = None
