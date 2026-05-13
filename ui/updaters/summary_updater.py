from core.app_state import (
    app_state
)

from utils.task_utils import (
    is_task_finished
)


# =========================================================
# UPDATE SUMMARY
# =========================================================

def update_summary(
    panel
):

    # =====================================================
    # TOTAL TASKS
    # =====================================================

    total_tasks = len(
        app_state.image_paths
    )

    # =====================================================
    # COMPLETED
    # =====================================================

    completed = 0

    for path in app_state.image_paths:

        status = app_state.task_status.get(
            path
        )

        if is_task_finished(
            status
        ):

            completed += 1

    # =====================================================
    # PROGRESS
    # =====================================================

    progress = 0

    if total_tasks > 0:

        progress = (
            completed / total_tasks
        )

    # =====================================================
    # LABEL
    # =====================================================

    panel.summary_label.configure(

        text=(
            f"{completed} / "
            f"{total_tasks} completed"
        )
    )

    # =====================================================
    # PROGRESSBAR
    # =====================================================

    panel.summary_progressbar.set(
        progress
    )