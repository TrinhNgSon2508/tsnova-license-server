import time

from core.app_state import (
    app_state
)


# =========================================================
# TASK COMPLETED
# =========================================================

def mark_task_completed(
    image_path
):

    app_state.completed_tasks += 1

    start_time = app_state.task_start_time.get(
        image_path
    )

    if not start_time:
        return

    elapsed = (
        time.time() - start_time
    )

    app_state.total_processing_time += (
        elapsed
    )

    if app_state.completed_tasks <= 0:
        return

    app_state.average_processing_time = (

        app_state.total_processing_time /

        app_state.completed_tasks
    )

    if app_state.average_processing_time > 0:

        app_state.processing_speed = (

            60 /

            app_state.average_processing_time
        )


# =========================================================
# TASK FAILED
# =========================================================

def mark_task_failed():

    app_state.failed_tasks += 1


# =========================================================
# TASK CANCELLED
# =========================================================

def mark_task_cancelled():

    app_state.cancelled_tasks += 1


# =========================================================
# RESET TASK STATS
# =========================================================

def reset_task_stats():

    app_state.completed_tasks = 0

    app_state.failed_tasks = 0

    app_state.cancelled_tasks = 0

    app_state.total_processing_time = 0

    app_state.average_processing_time = 0

    app_state.processing_speed = 0