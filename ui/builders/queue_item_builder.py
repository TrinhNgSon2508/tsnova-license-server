import customtkinter as ctk


# =========================================================
# CREATE QUEUE ITEM
# =========================================================

def create_queue_item(

    panel,

    image_path,

    label_text,

    status_color,

    progress
):

    # =====================================================
    # ITEM FRAME
    # =====================================================

    item_frame = ctk.CTkFrame(
        panel.scroll_frame
    )

    item_frame.pack(
        fill="x",
        padx=5,
        pady=5
    )

    # =====================================================
    # DRAG EVENTS
    # =====================================================

    item_frame.bind(

        "<Button-1>",

        lambda e, p=image_path:
        panel.start_drag(p)
    )

    item_frame.bind(

        "<ButtonRelease-1>",

        lambda e, p=image_path:
        panel.end_drag(p)
    )

    # =====================================================
    # LABEL
    # =====================================================

    label = ctk.CTkLabel(

        item_frame,

        text=label_text,

        text_color=status_color,

        anchor="w"
    )

    label.pack(
        fill="x",
        padx=10,
        pady=(10, 5)
    )

    # =====================================================
    # PROGRESSBAR
    # =====================================================

    progressbar = ctk.CTkProgressBar(
        item_frame,
        height=10
    )

    progressbar.pack(
        fill="x",
        padx=10,
        pady=(0, 10)
    )

    progressbar.set(
        progress / 100
    )

    # =====================================================
    # BUTTON FRAME
    # =====================================================

    button_frame = ctk.CTkFrame(

        item_frame,

        fg_color="transparent"
    )

    button_frame.pack(
        fill="x",
        padx=10,
        pady=(0, 10)
    )

    # =====================================================
    # RETRY BUTTON
    # =====================================================

    retry_button = ctk.CTkButton(

        button_frame,

        text="Retry",

        width=70,

        command=lambda:
        panel.retry_item(
            image_path
        )
    )

    retry_button.pack(
        side="right",
        padx=5
    )

    # =====================================================
    # CANCEL BUTTON
    # =====================================================

    cancel_button = ctk.CTkButton(

        button_frame,

        text="Cancel",

        width=70,

        command=lambda:
        panel.cancel_item(
            image_path
        )
    )

    cancel_button.pack(
        side="right",
        padx=5
    )

    # =====================================================
    # REMOVE BUTTON
    # =====================================================

    remove_button = ctk.CTkButton(

        button_frame,

        text="Remove",

        width=70,

        command=lambda:
        panel.remove_item(
            image_path
        )
    )

    remove_button.pack(
        side="right",
        padx=5
    )

    # =====================================================
    # RETURN
    # =====================================================

    return (
        item_frame,
        label,
        progressbar
    )