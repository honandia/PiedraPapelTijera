import logging
import os

# Asegurarse de que la carpeta 'logs' exista
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configuración global de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de los logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato de los logs
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log")),  # Guardar logs en logs/app.log
        #logging.StreamHandler()  # Mostrar los logs en la consola
    ]
)

# Función para obtener el logger en cualquier parte del proyecto
def get_logger(name: str):
    return logging.getLogger(name)
