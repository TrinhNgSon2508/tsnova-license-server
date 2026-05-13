# =========================================================
# UPDATE QUEUE ITEM
# =========================================================

def update_queue_item(

    label,

    progressbar,

    label_text,

    status_color,

    progress
):

    # =====================================================
    # LABEL
    # =====================================================

    label.configure(

        text=label_text,

        text_color=status_color
    )

    # =====================================================
    # PROGRESSBAR
    # =====================================================

    progressbar.set(
        progress / 100
    )