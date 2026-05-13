import time
import queue

from core.app_state import (
    app_state
)

from core.constants import (
    WORKER_SLEEP_EMPTY,
    WORKER_SLEEP_LIMIT,
    WORKER_SLEEP_START
)

from core.task_manager import (
    start_task,
    complete_task,
    fail_task,
    cancel_task
)

from core.task_stats import (
    mark_task_completed,
    mark_task_failed,
    mark_task_cancelled
)

from utils.threading_utils import (
    start_daemon_thread
)

from services.upscale_service import (
    upscale_image
)

from ui.preview_manager import (
    preview_manager
)


# =========================================================
# WORKER STATE
# =========================================================

worker_running = False


# =========================================================
# PROCESS FILE
# =========================================================

def process_file(
    file_path
):

    # =====================================================
    # CANCEL BEFORE START
    # =====================================================

    if file_path in app_state.cancel_requested:

        app_state.cancel_requested.remove(
            file_path
        )

        preview_manager.update_task_status(
            file_path,
            "cancelled"
        )

        preview_manager.update_task_progress(
            file_path,
            0
        )

        cancel_task(
            file_path
        )

        mark_task_cancelled()

        return

    # =====================================================
    # START PROCESSING
    # =====================================================

    preview_manager.update_task_status(
        file_path,
        "processing"
    )

    # =====================================================
    # UPSCALE
    # =====================================================

    success = upscale_image(
        file_path,
        progress_callback=lambda value:
        preview_manager.update_task_progress(
            file_path,
            value
        )
    )

    # =====================================================
    # CANCEL AFTER PROCESS
    # =====================================================

    if file_path in app_state.cancel_requested:

        app_state.cancel_requested.remove(
            file_path
        )

        preview_manager.update_task_status(
            file_path,
            "cancelled"
        )

        preview_manager.update_task_progress(
            file_path,
            0
        )

        cancel_task(
            file_path
        )

        mark_task_cancelled()

        return

    # =====================================================
    # SUCCESS
    # =====================================================

    if success:

        preview_manager.update_task_status(
            file_path,
            "completed"
        )

        preview_manager.update_task_progress(
            file_path,
            100
        )

        complete_task(
            file_path
        )

        mark_task_completed(
            file_path
        )

        return

    # =====================================================
    # FAILED
    # =====================================================

    preview_manager.update_task_status(
        file_path,
        "failed"
    )

    preview_manager.update_task_progress(
        file_path,
        0
    )

    fail_task(
        file_path
    )

    mark_task_failed()


# =========================================================
# TASK THREAD
# =========================================================

def task_worker(
    file_path
):

    try:

        # =================================================
        # ACTIVE WORKER +
        # =================================================

        with app_state.worker_lock:

            app_state.active_workers += 1

        # =================================================
        # PROCESS
        # =================================================

        process_file(
            file_path
        )

    except Exception as error:

        print(
            f"Worker Error: {error}"
        )

        preview_manager.update_task_status(
            file_path,
            "failed"
        )

        preview_manager.update_task_progress(
            file_path,
            0
        )

        fail_task(
            file_path
        )

        mark_task_failed()

    finally:

        # =================================================
        # ACTIVE WORKER -
        # =================================================

        with app_state.worker_lock:

            app_state.active_workers -= 1


# =========================================================
# MAIN LOOP
# =========================================================

def worker_loop():

    global worker_running

    while worker_running:

        # =================================================
        # PAUSED
        # =================================================

        if app_state.queue_paused:

            time.sleep(
                WORKER_SLEEP_EMPTY
            )

            continue

        # =================================================
        # WORKER LIMIT
        # =================================================

        with app_state.worker_lock:

            worker_limit_reached = (
                app_state.active_workers >=
                app_state.max_workers
            )

        if worker_limit_reached:

            time.sleep(
                WORKER_SLEEP_LIMIT
            )

            continue

        # =================================================
        # GET TASK
        # =================================================

        try:

            file_path = (
                app_state.processing_queue.get_nowait()
            )

        except queue.Empty:

            time.sleep(
                WORKER_SLEEP_EMPTY
            )

            continue

        # =================================================
        # SKIP REMOVED
        # =================================================

        if file_path not in app_state.image_paths:
            continue

        # =================================================
        # START TASK
        # =================================================

        start_task(
            file_path
        )

        # =================================================
        # START THREAD
        # =================================================

        start_daemon_thread(
            task_worker,
            (file_path,)
        )

        time.sleep(
            WORKER_SLEEP_START
        )


# =========================================================
# START WORKER
# =========================================================

def start_processing_worker():

    global worker_running

    if worker_running:
        return

    worker_running = True

    start_daemon_thread(
        worker_loop
    )


# =========================================================
# STOP WORKER
# =========================================================

def stop_processing_worker():

    global worker_running

    worker_running = False