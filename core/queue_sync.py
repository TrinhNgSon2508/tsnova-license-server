from core.app_state import app_state


def sync_queue_ui(queue_panel):

    current_ids = set()

    for task in app_state.tasks:

        task_id = task["id"]

        current_ids.add(task_id)

        if task_id not in queue_panel.queue_items:

            queue_panel.add_queue_item(task)

        else:

            queue_panel.update_queue_item(task)

    ui_ids = list(queue_panel.queue_items.keys())

    for task_id in ui_ids:

        if task_id not in current_ids:

            queue_panel.remove_queue_item(task_id)
