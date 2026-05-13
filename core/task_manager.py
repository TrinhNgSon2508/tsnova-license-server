from core.app_state import app_state


def get_task(task_id):

    for task in app_state.tasks:

        if task["id"] == task_id:
            return task

    return None


def get_tasks():

    return app_state.tasks


def add_task(task):

    app_state.tasks.append(task)


def remove_task(task_id):

    app_state.tasks = [
        task
        for task in app_state.tasks
        if task["id"] != task_id
    ]


def start_task(task_id):

    task = get_task(task_id)

    if task:
        task["status"] = "processing"


def complete_task(task_id):

    task = get_task(task_id)

    if task:
        task["status"] = "completed"
        task["progress"] = 100


def fail_task(task_id, error=None):

    task = get_task(task_id)

    if task:
        task["status"] = "failed"
        task["error"] = error


def cancel_task(task_id):

    task = get_task(task_id)

    if task:
        task["status"] = "cancelled"


def update_progress(task_id, progress):

    task = get_task(task_id)

    if task:
        task["progress"] = progress


def retry_task(task_id):

    task = get_task(task_id)

    if task:
        task["status"] = "waiting"
        task["progress"] = 0
        task["error"] = None


def clear_completed_tasks():

    app_state.tasks = [
        task
        for task in app_state.tasks
        if task.get("status") not in [
            "completed",
            "cancelled"
        ]
    ]
