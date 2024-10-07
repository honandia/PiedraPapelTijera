import os
from app.logger_config import get_logger
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Obtener el logger
logger = get_logger(__name__)

# Asegurarse de que la carpeta 'data' exista
log_dir = "data"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/game.db"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inicializar la base de datos (crea las tablas si no existen)
def init_db():
    """
    Inicializa la base de datos creando las tablas si no existen.
    
    La función utiliza la variable de entorno SQLALCHEMY_DATABASE_URL para
    determinar la base de datos a utilizar. La base de datos debe existir previamente.
    """
    logger.info("Inicializando la base de datos.")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")

def get_db():
    """
    Obtiene una sesión de la base de datos.

    Crea una sesión de la base de datos utilizando la variable de entorno
    SQLALCHEMY_DATABASE_URL. La sesión se cierra automáticamente al final de
    la función.

    Returns:
        Session: La sesión de la base de datos.
    """
    logger.info("Abriendo una nueva sesión de la base de datos.")
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error durante la sesión de base de datos: {e}")
    finally:
        logger.info("Cerrando la sesión de la base de datos.")
        db.close()
