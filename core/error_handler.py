import traceback

from core.logger import (
    logger
)


# =========================================================
# HANDLE ERROR
# =========================================================

def handle_error(

    error,

    context=""
):

    error_message = (
        f"{context}\n"
        f"{str(error)}"
    )

    logger.error(
        error_message
    )

    logger.error(
        traceback.format_exc()
    )