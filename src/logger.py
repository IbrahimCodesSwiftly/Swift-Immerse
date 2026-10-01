import logging
from pathlib import Path
from datetime import datetime


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Log directory
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# One log file per day
LOG_FILE = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"


logger = logging.getLogger("swift_immerse")
logger.setLevel(logging.DEBUG)


if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Detailed file logging
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Cleaner console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

if __name__ == "__main__":
    logger.debug("DEBUG test")
    logger.info("INFO test")
    logger.warning("WARNING test")
    logger.error("ERROR test")