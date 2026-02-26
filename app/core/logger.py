import logging
import sys
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """
    Retorna un logger configurado con formato legible para la terminal.
    Uso: logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            "\n%(asctime)s | %(levelname)-8s | %(name)s\n%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger


def setup_db_logger():
    """
    Configura el logger de SQLAlchemy para escribir en logs/db.log
    en vez de la terminal. Debe llamarse al iniciar el servidor.
    """
    logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    log_file = logs_dir / "db.log"

    db_logger = logging.getLogger("sqlalchemy.engine")
    db_logger.setLevel(logging.INFO)
    db_logger.propagate = False

    # Limpiar handlers previos (por si se llama más de una vez con --reload)
    db_logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    db_logger.addHandler(file_handler)
