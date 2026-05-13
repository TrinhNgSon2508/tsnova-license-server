from core.app_state import (
    app_state
)

from core.database import (
    database_manager
)


# =========================================================
# RESTORE TASKS
# =========================================================

def restore_unfinished_tasks():

    tasks = (
        database_manager.get_unfinished_tasks()
    )

    restored_count = 0

    for task in tasks:

        input_path = task[
            "input_path"
        ]

        # =================================================
        # RESTORE PATH
        # =================================================

        if input_path not in app_state.image_paths:

            app_state.image_paths.append(
                input_path
            )

        # =================================================
        # REQUEUE
        # =================================================

        app_state.processing_queue.put(
            input_path
        )

        app_state.task_status[
            input_path
        ] = "waiting"

        restored_count += 1

    print(
        f"Restored {restored_count} tasks"
    )