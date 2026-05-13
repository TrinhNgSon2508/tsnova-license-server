import json
import os

from core.app_state import (
    app_state
)


# =========================================================
# SAVE PATH
# =========================================================

QUEUE_FILE = "queue_data.json"


# =========================================================
# SAVE QUEUE
# =========================================================

def save_queue():

    data = {

        "image_paths":
        app_state.image_paths,

        "task_status":
        app_state.task_status,

        "task_progress":
        app_state.task_progress
    }

    with open(
        QUEUE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# =========================================================
# LOAD QUEUE
# =========================================================

def load_queue():

    if not os.path.exists(
        QUEUE_FILE
    ):

        return

    try:

        with open(
            QUEUE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        app_state.image_paths = data.get(
            "image_paths",
            []
        )

        app_state.task_status = data.get(
            "task_status",
            {}
        )

        app_state.task_progress = data.get(
            "task_progress",
            {}
        )

        # =============================================
        # REBUILD WAITING QUEUE
        # =============================================

        app_state.processing_queue.clear()

        for path in app_state.image_paths:

            status = app_state.task_status.get(
                path,
                "waiting"
            )

            if status in [
                "waiting",
                "processing"
            ]:

                app_state.task_status[
                    path
                ] = "waiting"

                app_state.processing_queue.append(
                    path
                )

    except Exception:

        pass