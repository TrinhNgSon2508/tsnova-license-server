import threading

from core.app_state import app_state

from core.logger import logger

from workers.processing_worker import (
    processing_worker
)


# =========================================================
# PROCESSING CONTROLLER
# =========================================================

class ProcessingController:

    def __init__(self):

        self.worker_thread = None

    # =====================================================
    # START
    # =====================================================

    def start_processing(self):

        if app_state.processing:

            logger.log(
                "Processing already running"
            )

            return

        logger.log(
            "Starting processing"
        )

        self.worker_thread = threading.Thread(

            target=processing_worker.start,

            daemon=True
        )

        self.worker_thread.start()

    # =====================================================
    # STOP
    # =====================================================

    def stop_processing(self):

        if not app_state.processing:

            logger.log(
                "No active processing"
            )

            return

        app_state.stop_requested = True

        logger.log(
            "Stop requested"
        )

    # =====================================================
    # PAUSE
    # =====================================================

    def pause_processing(self):

        if not app_state.processing:

            logger.log(
                "No active processing"
            )

            return

        app_state.paused = True

        logger.log(
            "Paused"
        )

    # =====================================================
    # RESUME
    # =====================================================

    def resume_processing(self):

        if not app_state.processing:

            logger.log(
                "No active processing"
            )

            return

        app_state.paused = False

        logger.log(
            "Resumed"
        )


# =========================================================
# GLOBAL INSTANCE
# =========================================================

processing_controller = ProcessingController()