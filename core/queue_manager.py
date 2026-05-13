from core.app_state import (
    app_state
)

from core.task_manager import (
    reset_task,
    cancel_task
)

from core.queue_sync import (
    rebuild_processing_queue
)


# =========================================================
# REMOVE ITEM
# =========================================================

def remove_item(
    image_path
):

    # =====================================================
    # REMOVE FROM IMAGE PATHS
    # =====================================================

    if image_path in app_state.image_paths:

        app_state.image_paths.remove(
            image_path
        )

    # =====================================================
    # REMOVE FROM PROCESSING QUEUE
    # =====================================================

    if image_path in app_state.processing_queue:

        app_state.processing_queue.remove(
            image_path
        )

    # =====================================================
    # REMOVE TASK DATA
    # =====================================================

    app_state.task_status.pop(
        image_path,
        None
    )

    app_state.task_progress.pop(
        image_path,
        None
    )

    app_state.task_start_time.pop(
        image_path,
        None
    )

    app_state.cancel_requested.discard(
        image_path
    )

    # =====================================================
    # SYNC QUEUE
    # =====================================================

    rebuild_processing_queue()


# =========================================================
# RETRY ITEM
# =========================================================

def retry_item(
    image_path
):

    # =====================================================
    # RESET TASK
    # =====================================================

    reset_task(
        image_path
    )

    # =====================================================
    # ADD TO IMAGE PATHS
    # =====================================================

    if image_path not in app_state.image_paths:

        app_state.image_paths.append(
            image_path
        )

    # =====================================================
    # ADD TO QUEUE
    # =====================================================

    if image_path not in app_state.processing_queue:

        app_state.processing_queue.append(
            image_path
        )

    # =====================================================
    # REMOVE CANCEL FLAG
    # =====================================================

    app_state.cancel_requested.discard(
        image_path
    )

    # =====================================================
    # SYNC QUEUE
    # =====================================================

    rebuild_processing_queue()


# =========================================================
# CANCEL ITEM
# =========================================================

def cancel_queue_item(
    image_path
):

    # =====================================================
    # REQUEST CANCEL
    # =====================================================

    app_state.cancel_requested.add(
        image_path
    )

    # =====================================================
    # CANCEL WAITING TASK
    # =====================================================

    if image_path in app_state.processing_queue:

        if image_path in app_state.processing_queue:

            app_state.processing_queue.remove(
                image_path
            )

        cancel_task(
            image_path
        )

    # =====================================================
    # SYNC QUEUE
    # =====================================================

    rebuild_processing_queue()


# =========================================================
# CLEAR QUEUE
# =========================================================

def clear_queue():

    # =====================================================
    # CLEAR LISTS
    # =====================================================

    app_state.image_paths.clear()

    app_state.processing_queue.clear()

    app_state.cancel_requested.clear()

    # =====================================================
    # CLEAR TASK STATE
    # =====================================================

    app_state.task_status.clear()

    app_state.task_progress.clear()

    app_state.task_start_time.clear()

    # =====================================================
    # RESET STATS
    # =====================================================

    app_state.active_workers = 0

    app_state.completed_tasks = 0

    app_state.failed_tasks = 0

    app_state.cancelled_tasks = 0

    app_state.total_processing_time = 0

    app_state.average_processing_time = 0

    app_state.processing_speed = 0