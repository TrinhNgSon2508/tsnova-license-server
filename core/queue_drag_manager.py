from core.app_state import (
    app_state
)


# =========================================================
# MOVE QUEUE ITEM
# =========================================================

def move_queue_item(

    source_path,

    target_path
):

    queue = app_state.image_paths

    # =====================================================
    # VALIDATE
    # =====================================================

    if (
        source_path not in queue or
        target_path not in queue
    ):

        return

    if source_path == target_path:
        return

    # =====================================================
    # GET INDEX
    # =====================================================

    source_index = queue.index(
        source_path
    )

    target_index = queue.index(
        target_path
    )

    # =====================================================
    # MOVE ITEM
    # =====================================================

    queue.insert(
        target_index,
        queue.pop(source_index)
    )

    # =====================================================
    # SAVE ORDER
    # =====================================================

    app_state.image_paths = list(
        queue
    )

    # =====================================================
    # REBUILD WAITING QUEUE
    # =====================================================

    rebuild_processing_queue()