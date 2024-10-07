from app.logger_config import get_logger
from app.models import JugadaEnum, Jugador, Partida, Jugada
from app.repositories import PartidaRepository, JugadorRepository

# Obtener el logger
logger = get_logger(__name__)

class JuegoService:

    def __init__(self, partida_repo: PartidaRepository, jugador_repo: JugadorRepository):
        """
        Inicializa el servicio del juego con los repositorios de partidas y jugadores.

        Args:
            partida_repo (PartidaRepository): Repositorio de partidas.
            jugador_repo (JugadorRepository): Repositorio de jugadores.
        """
        self.partida_repo = partida_repo
        self.jugador_repo = jugador_repo
        logger.info("JuegoService inicializado.")

    def iniciar_partida(self, jugador1: Jugador, jugador2: Jugador):
        """
        Inicia una partida de Piedra, Papel o Tijera entre dos jugadores.

        Args:
            jugador1 (Jugador): El primer jugador.
            jugador2 (Jugador): El segundo jugador.

        Returns:
            Partida: La partida que se ha iniciado.
        """
        logger.info(f"Iniciando partida entre {jugador1.nombre} y {jugador2.nombre}.")
        try:
            partida = Partida(estado='en curso')
            self.partida_repo.save(partida)
            logger.info(f"Partida iniciada con éxito: {partida}")
            return partida
        except Exception as e:
            logger.error(f"Error al iniciar la partida: {e}")
            raise e

    def registrar_jugada(self, partida: Partida, jugador: Jugador, jugada_jugador: JugadaEnum, jugada_maquina: JugadaEnum):
        """
        Registra una jugada de un jugador en una partida.

        Args:
            partida (Partida): La partida en la que se va a registrar la jugada.
            jugador (Jugador): El jugador que va a registrar la jugada.
            jugada_jugador (JugadaEnum): La jugada del jugador.
            jugada_maquina (JugadaEnum): La jugada de la máquina.

        Returns:
            str: El resultado de la jugada ('ganada', 'perdida' o 'empate').
        """
        logger.info(f"Registrando jugada de {jugador.nombre} en la partida {partida.id}. Jugada jugador: {jugada_jugador}, Jugada máquina: {jugada_maquina}.")
        try:
            resultado = self.determinar_resultado(jugada_jugador, jugada_maquina)
            jugada = Jugada(partida_id=partida.id, jugador_id=jugador.id, tipo=jugada_jugador, resultado=resultado)
            self.partida_repo.save(jugada)
            logger.info(f"Jugada registrada con éxito: {jugada}. Resultado: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al registrar la jugada: {e}")
            raise e

    def determinar_resultado(self, jugada_jugador, jugada_maquina):
        """
        Determina el resultado de una jugada.

        Args:
            jugada_jugador (JugadaEnum): La jugada del jugador.
            jugada_maquina (JugadaEnum): La jugada de la máquina.

        Returns:
            str: El resultado de la jugada ('ganada', 'perdida' o 'empate').
        """
        logger.info(f"Determinando resultado. Jugada jugador: {jugada_jugador}, Jugada máquina: {jugada_maquina}.")
        if jugada_jugador == jugada_maquina:
            logger.info("Resultado: empate.")
            return 'empate'
        elif (jugada_jugador == JugadaEnum.PIEDRA and jugada_maquina == JugadaEnum.TIJERA) or \
             (jugada_jugador == JugadaEnum.PAPEL and jugada_maquina == JugadaEnum.PIEDRA) or \
             (jugada_jugador == JugadaEnum.TIJERA and jugada_maquina == JugadaEnum.PAPEL):
            logger.info("Resultado: ganada.")
            return 'ganada'
        else:
            logger.info("Resultado: perdida.")
            return 'perdida'

    def finalizar_partida(self, partida: Partida, ganador: Jugador):
        """
        Finaliza una partida asignando el ganador y sumando un punto a este.

        Args:
            partida (Partida): La partida que se va a finalizar.
            ganador (Jugador): El jugador que ha ganado la partida.
        """
        logger.info(f"Finalizando partida {partida.id}. Ganador: {ganador.nombre}.")
        try:
            partida.ganador_id = ganador.id
            partida.estado = 'finalizada'
            ganador.puntos += 1
            self.partida_repo.save(partida)
            logger.info(f"Partida finalizada. Ganador {ganador.nombre}, Puntos totales: {ganador.puntos}")
        except Exception as e:
            logger.error(f"Error al finalizar la partida {partida.id}: {e}")
            raise e

    def marcar_abandonada(self, partida: Partida):
        """
        Marca una partida como abandonada.

        Args:
            partida (Partida): La partida que se va a marcar como abandonada.
        """
        logger.info(f"Marcando partida {partida.id} como abandonada.")
        try:
            partida.estado = 'abandonada'
            self.partida_repo.save(partida)
            logger.info(f"Partida {partida.id} marcada como abandonada.")
        except Exception as e:
            logger.error(f"Error al marcar la partida {partida.id} como abandonada: {e}")
            raise e
