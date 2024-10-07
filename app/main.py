from app.logger_config import get_logger
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.repositories import PartidaRepository, JugadorRepository
from app.database import get_db

# Obtener el logger
logger = get_logger(__name__)

app = FastAPI()

@app.get("/get_global_info")
def get_global_info(db: Session = Depends(get_db)):
    """
    Obtiene información global de las partidas.

    Returns:
        dict[str, int|float]: Un diccionario con la siguiente estructura:
            {
                "total_victorias": int,  # Número de partidas ganadas.
                "total_derrotas": int,  # Número de partidas perdidas.
                "total_partidas": int,  # Número total de partidas.
                "winrate": float  # Porcentaje de partidas ganadas.
            }
    """
    logger.info("GET /get_global_info - Solicitud de información global de las partidas.")
    partida_repo = PartidaRepository(db)
    try:
        info = partida_repo.obtener_info_global()
        logger.info(f"Información global obtenida: {info}")
        return info
    except Exception as e:
        logger.error(f"Error al obtener información global: {e}")
        raise e

@app.get("/mano_fuerte")
def mano_fuerte(db: Session = Depends(get_db)):
    """
    Obtiene la mano que más veces ha ganado y su porcentaje de victoria.

    Returns:
        dict[str, str|float]: Un diccionario con la siguiente estructura:
            {
                "mano_fuerte": str,  # La mano que más veces ha ganado.
                "porcentaje_victorias": float  # El porcentaje de victorias de la mano fuerte.
            }
    """
    logger.info("GET /mano_fuerte - Solicitud de la mano más fuerte.")
    partida_repo = PartidaRepository(db)
    try:
        mano, porcentaje = partida_repo.obtener_mano_fuerte()
        logger.info(f"Mano fuerte: {mano}, Porcentaje de victorias: {porcentaje}")
        return {"mano_fuerte": mano, "porcentaje_victorias": porcentaje}
    except Exception as e:
        logger.error(f"Error al obtener mano fuerte: {e}")
        raise e

@app.get("/mano_debil")
def mano_debil(db: Session = Depends(get_db)):
    """
    Obtiene la mano que más veces ha perdido y su porcentaje de derrota.

    Returns:
        dict[str, str|float]: Un diccionario con la siguiente estructura:
            {
                "mano_debil": str,  # La mano que más veces ha perdido.
                "porcentaje_derrotas": float  # El porcentaje de derrotas de la mano débil.
            }
    """
    logger.info("GET /mano_debil - Solicitud de la mano más débil.")
    partida_repo = PartidaRepository(db)
    try:
        mano, porcentaje = partida_repo.obtener_mano_debil()
        logger.info(f"Mano débil: {mano}, Porcentaje de derrotas: {porcentaje}")
        return {"mano_debil": mano, "porcentaje_derrotas": porcentaje}
    except Exception as e:
        logger.error(f"Error al obtener mano débil: {e}")
        raise e

@app.get("/ranking")
def ranking(db: Session = Depends(get_db)):
    """
    Obtiene el ranking de los 3 jugadores con más puntos.

    Returns:
        list[Jugador]: Una lista con los 3 jugadores con más puntos.
    """
    logger.info("GET /ranking - Solicitud del ranking de jugadores.")
    jugador_repo = JugadorRepository(db)
    try:
        ranking = jugador_repo.obtener_ranking()
        logger.info(f"Ranking obtenido: {ranking}")
        return ranking
    except Exception as e:
        logger.error(f"Error al obtener ranking de jugadores: {e}")
        raise e

@app.get("/estadisticas")
def estadisticas(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas de partidas.

    Returns:
        dict[str, int]: Un diccionario con las estadísticas de partidas:
            - total_partidas: Número total de partidas.
            - partidas_ganadas: Número de partidas ganadas.
            - partidas_abandonadas: Número de partidas abandonadas.
    """
    logger.info("GET /estadisticas - Solicitud de estadísticas de partidas.")
    partida_repo = PartidaRepository(db)
    try:
        estadisticas = partida_repo.obtener_estadisticas_partidas()
        logger.info(f"Estadísticas obtenidas: {estadisticas}")
        return estadisticas
    except Exception as e:
        logger.error(f"Error al obtener estadísticas de partidas: {e}")
        raise e
