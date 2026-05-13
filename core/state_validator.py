from core.app_state import (
    app_state
)


# =========================================================
# VALIDATE ACTIVE WORKERS
# =========================================================

def validate_active_workers():

    if app_state.active_workers < 0:

        app_state.active_workers = 0


# =========================================================
# VALIDATE PROGRESS
# =========================================================

def validate_task_progress():

    for path, progress in list(

        app_state.task_progress.items()
    ):

        if progress < 0:

            app_state.task_progress[
                path
            ] = 0

        elif progress > 100:

            app_state.task_progress[
                path
            ] = 100


# =========================================================
# REMOVE ORPHAN TASKS
# =========================================================

def remove_orphan_tasks():

    valid_paths = set(
        app_state.image_paths
    )

    # =====================================================
    # STATUS
    # =====================================================

    for path in list(
        app_state.task_status.keys()
    ):

        if path not in valid_paths:

            app_state.task_status.pop(
                path,
                None
            )

    # =====================================================
    # PROGRESS
    # =====================================================

    for path in list(
        app_state.task_progress.keys()
    ):

        if path not in valid_paths:

            app_state.task_progress.pop(
                path,
                None
            )

    # =====================================================
    # START TIME
    # =====================================================

    for path in list(
        app_state.task_start_time.keys()
    ):

        if path not in valid_paths:

            app_state.task_start_time.pop(
                path,
                None
            )


# =========================================================
# REMOVE DUPLICATE QUEUE
# =========================================================

def remove_duplicate_queue_items():

    unique_queue = []

    seen = set()

    for path in app_state.processing_queue:

        if path in seen:
            continue

        seen.add(path)

        unique_queue.append(
            path
        )

    app_state.processing_queue = (
        unique_queue
    )


# =========================================================
# VALIDATE ALL STATE
# =========================================================

def validate_app_state():

    validate_active_workers()

    validate_task_progress()

    remove_orphan_tasks()

    remove_duplicate_queue_items()