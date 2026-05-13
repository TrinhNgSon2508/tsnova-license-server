from core.app_state import app_state


def update_monitor():

    stats = app_state.stats

    app_state.monitor_data = {
        "total": stats.get("total", 0),
        "completed": stats.get("completed", 0),
        "failed": stats.get("failed", 0),
        "processing": stats.get("processing", 0),
        "waiting": stats.get("waiting", 0)
    }
