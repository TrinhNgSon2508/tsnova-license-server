from core.app_state import app_state


def update_summary():

    total = len(app_state.tasks)

    waiting = 0
    processing = 0
    completed = 0
    failed = 0

    for task in app_state.tasks:

        status = task.get("status", "waiting").lower()

        if status == "waiting":
            waiting += 1

        elif status == "processing":
            processing += 1

        elif status == "completed":
            completed += 1

        elif status == "failed":
            failed += 1

    app_state.stats = {
        "total": total,
        "waiting": waiting,
        "processing": processing,
        "completed": completed,
        "failed": failed
    }
