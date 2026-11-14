"""
Configuracion del archivo de logs.

Todos los modulos usan obtener_logger() para escribir errores y eventos
relevantes en logs/software_fj.log (no se usa ninguna base de datos).
"""

import logging                      # Libreria estandar para registrar mensajes
from pathlib import Path            # Manejo de rutas independiente del sistema operativo

# Ruta del archivo: <carpeta del proyecto>/logs/software_fj.log
RUTA_LOGS = Path(__file__).resolve().parent.parent / "logs" / "software_fj.log"


def obtener_logger(nombre="software_fj"):
    """Devuelve el logger de la aplicacion, configurandolo la primera vez."""
    logger = logging.getLogger(nombre)       # Pide (o crea) el logger con ese nombre
    if logger.handlers:                      # Si ya fue configurado antes...
        return logger                        # ...lo reutilizamos sin duplicar mensajes

    logger.setLevel(logging.DEBUG)           # Registra todos los niveles (DEBUG en adelante)
    RUTA_LOGS.parent.mkdir(parents=True, exist_ok=True)   # Crea la carpeta logs/ si no existe

    # El handler escribe en el archivo; utf-8 para conservar tildes y la letra n con tilde
    manejador = logging.FileHandler(RUTA_LOGS, encoding="utf-8")
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"   # fecha | nivel | mensaje
    )
    manejador.setFormatter(formato)          # Aplica el formato al handler
    logger.addHandler(manejador)             # Conecta el handler con el logger
    logger.propagate = False                 # Evita que el mensaje salga duplicado por el logger raiz
    return logger
