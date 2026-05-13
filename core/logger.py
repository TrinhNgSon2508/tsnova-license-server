import logging
import os


# =========================================================
# LOG DIR
# =========================================================

LOG_DIR = "logs"

os.makedirs(
    LOG_DIR,
    exist_ok=True
)


# =========================================================
# LOGGER
# =========================================================

logger = logging.getLogger(
    "TSNOVA"
)

logger.setLevel(
    logging.INFO
)


# =========================================================
# FORMATTER
# =========================================================

formatter = logging.Formatter(

    "[%(asctime)s] "

    "[%(levelname)s] "

    "%(message)s"
)


# =========================================================
# FILE HANDLER
# =========================================================

file_handler = logging.FileHandler(

    os.path.join(
        LOG_DIR,
        "tsnova.log"
    ),

    encoding="utf-8"
)

file_handler.setFormatter(
    formatter
)

logger.addHandler(
    file_handler
)


# =========================================================
# CONSOLE HANDLER
# =========================================================

console_handler = logging.StreamHandler()

console_handler.setFormatter(
    formatter
)

logger.addHandler(
    console_handler
)