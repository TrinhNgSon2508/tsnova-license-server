import os
import time

from core.app_state import app_state

from core.logger import logger

from services.image_service import image_service

from core.image_processor import process_image


# =========================================================
# PROCESSING WORKER
# =========================================================

class ProcessingWorker:

    def __init__(self):

        self.running = False

    # =====================================================
    # START LOOP
    # =====================================================

    def start(self):

        if self.running:

            logger.log(
                "Worker already running"
            )

            return

        self.running = True

        app_state.processing = True

        app_state.stop_requested = False

        app_state.paused = False

        # =================================================
        # RESET PROGRESS
        # =================================================

        app_state.completed_tasks = 0

        app_state.progress_percent = 0

        # =================================================
        # GET FILES
        # =================================================

        files = image_service.get_files()

        app_state.total_tasks = len(files)

        if not files:

            logger.log(
                "No files to process"
            )

            self.finish()

            return

        logger.log(
            f"Worker started ({len(files)} files)"
        )

        # =================================================
        # PROCESS LOOP
        # =================================================

        for index, file_path in enumerate(files):

            # =============================================
            # STOP
            # =============================================

            if app_state.stop_requested:

                logger.log(
                    "Processing stopped"
                )

                break

            # =============================================
            # PAUSE
            # =============================================

            while app_state.paused:

                time.sleep(0.1)

                if app_state.stop_requested:

                    break

            # =============================================
            # STOP AFTER PAUSE
            # =============================================

            if app_state.stop_requested:

                logger.log(
                    "Processing stopped"
                )

                break

            # =============================================
            # CURRENT FILE
            # =============================================

            app_state.current_file = file_path
            app_state.image_status[
                file_path
            ] = "processing"

            filename = os.path.basename(
                file_path
            )

            logger.log(
                f"Processing {filename}"
            )

            # =============================================
            # PROCESS IMAGE
            # =============================================

            try:

                success = process_image(
                    file_path
                )

                if success:

                    app_state.completed_tasks += 1

                    # =====================================
                    # PROGRESS %
                    # =====================================

                    if app_state.total_tasks > 0:

                        app_state.progress_percent = int(
                            (
                                app_state.completed_tasks
                                / app_state.total_tasks
                            ) * 100
                        )

                    app_state.image_status[
                        file_path
                    ] = "done"

                    logger.log(
                        f"Completed {filename}"
                    )

                else:

                    app_state.image_status[
                        file_path
                    ] = "failed"
                    logger.log(
                        f"Failed {filename}"
                    )

            except Exception as e:
                app_state.image_status[
                    file_path
                ] = "failed"

                logger.log(
                    f"Error processing {filename}: {e}"
                )

        # =================================================
        # FINISH
        # =================================================

        self.finish()

    # =====================================================
    # FINISH
    # =====================================================

    def finish(self):

        self.running = False

        app_state.processing = False

        app_state.current_file = ""

        if app_state.completed_tasks >= app_state.total_tasks:

            app_state.progress_percent = 100

        logger.log(
            "Worker finished"
        )


# =========================================================
# GLOBAL INSTANCE
# =========================================================

processing_worker = ProcessingWorker()