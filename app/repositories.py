from app.logger_config import get_logger
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Partida, Jugador, Jugada
from app.schemas import ResultadoJugadaEnum, EstadoPartidaEnum

# Obtener el logger
logger = get_logger(__name__)

class PartidaRepository:

    def __init__(self, db: Session):
        """
        Inicializa un objeto de tipo PartidaRepository.
        db: Session - La sesión de la base de datos.
        """
        self.db = db
        logger.info("PartidaRepository inicializado.")

    def obtener_info_global(self):
        """Obtiene información global de las partidas.

        Returns:
            dict[str, int|float]: Un diccionario con la siguiente estructura:
                {
                    "total_victorias": int,  # Número de partidas ganadas.
                    "total_derrotas": int,  # Número de partidas perdidas.
                    "total_partidas": int,  # Número total de partidas.
                    "winrate": float  # Porcentaje de partidas ganadas.
                }
        """
        logger.info("Consultando información global de las partidas.")
        try:
            total_victorias = self.db.query(func.count(Partida.id)).filter(Partida.ganador_id.isnot(None)).scalar()
            total_derrotas = self.db.query(func.count(Partida.id)).filter(Partida.estado == EstadoPartidaEnum.ABANDONADA).scalar()
            total_partidas = self.db.query(func.count(Partida.id)).scalar()
            winrate = (total_victorias / total_partidas) * 100 if total_partidas > 0 else 0
            info = {
                "total_victorias": total_victorias,
                "total_derrotas": total_derrotas,
                "total_partidas": total_partidas,
                "winrate": winrate
            }
            logger.info(f"Información global obtenida: {info}")
            return info
        except Exception as e:
            logger.error(f"Error al obtener información global: {e}")
            raise e

    def obtener_mano_fuerte(self):
        """Obtiene la mano que más veces ha ganado y su porcentaje de victoria.

        Returns:
            tuple[JugadaEnum, float]: Un tuple con la mano que más veces ha ganado y su
                porcentaje de victoria.
        """
        logger.info("Consultando la mano más fuerte.")
        try:
            mano_victoriosa = self.db.query(Jugada.tipo, func.count(Jugada.tipo)).filter(Jugada.resultado == ResultadoJugadaEnum.GANADA).group_by(Jugada.tipo).order_by(func.count(Jugada.tipo).desc()).first()
            total_victorias = self.db.query(func.count(Jugada.id)).filter(Jugada.resultado == ResultadoJugadaEnum.GANADA).scalar()
            porcentaje = (mano_victoriosa[1] / total_victorias) * 100 if total_victorias > 0 else 0
            logger.info(f"Mano fuerte obtenida: {mano_victoriosa[0]}, Porcentaje: {porcentaje}")
            return mano_victoriosa[0], porcentaje
        except Exception as e:
            logger.error(f"Error al obtener la mano fuerte: {e}")
            raise e

    def obtener_mano_debil(self):
        """Obtiene la mano que más veces ha perdido y su porcentaje de derrota.

        Returns:
            tuple[JugadaEnum, float]: Un tuple con la mano que más veces ha perdido y su
                porcentaje de derrota.
        """
        logger.info("Consultando la mano más débil.")
        try:
            mano_derrota = self.db.query(Jugada.tipo, func.count(Jugada.tipo)).filter(Jugada.resultado == ResultadoJugadaEnum.PERDIDA).group_by(Jugada.tipo).order_by(func.count(Jugada.tipo).desc()).first()
            total_derrotas = self.db.query(func.count(Jugada.id)).filter(Jugada.resultado == ResultadoJugadaEnum.PERDIDA).scalar()
            porcentaje = (mano_derrota[1] / total_derrotas) * 100 if total_derrotas > 0 else 0
            logger.info(f"Mano débil obtenida: {mano_derrota[0]}, Porcentaje: {porcentaje}")
            return mano_derrota[0], porcentaje
        except Exception as e:
            logger.error(f"Error al obtener la mano débil: {e}")
            raise e

    def obtener_estadisticas_partidas(self):
        """Obtiene estadísticas de partidas.

        Returns:
            dict: Un diccionario con las estadísticas de partidas:
                - total_partidas: Número total de partidas.
                - partidas_ganadas: Número de partidas ganadas.
                - partidas_abandonadas: Número de partidas abandonadas.
        """
        logger.info("Consultando estadísticas de partidas.")
        try:
            total_partidas = self.db.query(func.count(Partida.id)).scalar()
            ganadas = self.db.query(func.count(Partida.id)).filter(Partida.ganador_id.isnot(None)).scalar()
            abandonadas = self.db.query(func.count(Partida.id)).filter(Partida.estado == EstadoPartidaEnum.ABANDONADA).scalar()
            estadisticas = {
                "total_partidas": total_partidas,
                "partidas_ganadas": ganadas,
                "partidas_abandonadas": abandonadas
            }
            logger.info(f"Estadísticas obtenidas: {estadisticas}")
            return estadisticas
        except Exception as e:
            logger.error(f"Error al obtener estadísticas de partidas: {e}")
            raise e
    
    def save(self, partida):
        """
        Guarda una partida en la base de datos.

        Args:
            partida (Partida): La partida a guardar.

        Returns:
            Partida: La partida guardada con su id.
        """
        logger.info(f"Guardando la partida: {partida}")
        try:
            self.db.add(partida)
            self.db.commit()
            self.db.refresh(partida)
            logger.info(f"Partida guardada con éxito: {partida}")
            return partida
        except Exception as e:
            logger.error(f"Error al guardar la partida: {e}")
            self.db.rollback()
            raise e


class JugadorRepository:

    def __init__(self, db: Session):
        """
        Inicializa un objeto de tipo JugadorRepository.
        
        Args:
            db (Session): La sesión de la base de datos.
        """
        self.db = db
        logger.info("JugadorRepository inicializado.")

    def obtener_ranking(self):
        """
        Obtiene el ranking de los 3 jugadores con más puntos.

        Returns:
            list[Jugador]: Una lista con los 3 jugadores con más puntos.
        """
        logger.info("Consultando el ranking de jugadores.")
        try:
            ranking = self.db.query(Jugador).order_by(Jugador.puntos.desc()).limit(3).all()
            logger.info(f"Ranking obtenido: {ranking}")
            return ranking
        except Exception as e:
            logger.error(f"Error al obtener el ranking de jugadores: {e}")
            raise e

    def get_or_create(self, nombre, tipo):
        """
        Obtiene un jugador por su nombre, si no existe lo crea.

        Args:
            nombre (str): El nombre del jugador.
            tipo (str): El tipo del jugador ('humano' o 'maquina').

        Returns:
            Jugador: El jugador obtenido o creado.
        """
        logger.info(f"Consultando/Creando jugador: {nombre}, Tipo: {tipo}")
        try:
            jugador = self.db.query(Jugador).filter(Jugador.nombre == nombre).first()
            if not jugador:
                logger.info(f"Jugador no encontrado, creando nuevo jugador: {nombre}")
                jugador = Jugador(nombre=nombre, tipo=tipo)
                self.db.add(jugador)
                self.db.commit()
                self.db.refresh(jugador)
            logger.info(f"Jugador obtenido o creado: {jugador}")
            return jugador
        except Exception as e:
            logger.error(f"Error al obtener o crear jugador: {e}")
            raise e
