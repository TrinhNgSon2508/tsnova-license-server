import customtkinter as ctk

from core.app_state import (
    app_state
)

from ui.components.queue_item import (
    QueueItem
)


# =========================================================
# QUEUE LIST
# =========================================================

class QueueList(ctk.CTkScrollableFrame):

    def __init__(
        self,
        parent,
        retry_callback,
        cancel_callback,
        remove_callback,
        start_drag_callback,
        end_drag_callback
    ):

        super().__init__(
            parent,
            height=300
        )

        self.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =================================================
        # CALLBACKS
        # =================================================

        self.retry_callback = (
            retry_callback
        )

        self.cancel_callback = (
            cancel_callback
        )

        self.remove_callback = (
            remove_callback
        )

        self.start_drag_callback = (
            start_drag_callback
        )

        self.end_drag_callback = (
            end_drag_callback
        )

        # =================================================
        # ITEM REFERENCES
        # =================================================

        self.items = {}

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(
        self
    ):

        existing_paths = set(
            self.items.keys()
        )

        current_paths = set(
            app_state.image_paths
        )

        # =================================================
        # REMOVE OLD
        # =================================================

        removed_paths = (
            existing_paths - current_paths
        )

        for path in removed_paths:

            self.items[path].destroy()

            self.items.pop(
                path,
                None
            )

        # =================================================
        # BUILD / UPDATE
        # =================================================

        for image_path in app_state.image_paths:

            # =============================================
            # UPDATE EXISTING
            # =============================================

            if image_path in self.items:

                self.items[
                    image_path
                ].refresh()

                continue

            # =============================================
            # CREATE ITEM
            # =============================================

            item = QueueItem(

                self,

                image_path=image_path,

                retry_callback=(
                    self.retry_callback
                ),

                cancel_callback=(
                    self.cancel_callback
                ),

                remove_callback=(
                    self.remove_callback
                ),

                start_drag_callback=(
                    self.start_drag_callback
                ),

                end_drag_callback=(
                    self.end_drag_callback
                )
            )

            self.items[
                image_path
            ] = item