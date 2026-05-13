import os
import time

import customtkinter as ctk

from core.app_state import (
    app_state
)


# =========================================================
# QUEUE ITEM
# =========================================================

class QueueItem(ctk.CTkFrame):

    def __init__(

        self,

        parent,

        image_path,

        drag_callback,

        drop_callback,

        retry_callback,

        cancel_callback,

        remove_callback
    ):

        super().__init__(parent)

        self.image_path = image_path

        # =================================================
        # LAYOUT
        # =================================================

        self.pack(
            fill="x",
            padx=5,
            pady=5
        )

        # =================================================
        # DRAG EVENTS
        # =================================================

        self.bind(
            "<Button-1>",
            lambda e:
            drag_callback(self.image_path)
        )

        self.bind(
            "<ButtonRelease-1>",
            lambda e:
            drop_callback(self.image_path)
        )

        # =================================================
        # LABEL
        # =================================================

        self.label = ctk.CTkLabel(

            self,

            text="",

            anchor="w"
        )

        self.label.pack(
            fill="x",
            padx=10,
            pady=(10, 5)
        )

        # =================================================
        # PROGRESS BAR
        # =================================================

        self.progressbar = ctk.CTkProgressBar(
            self,
            height=10
        )

        self.progressbar.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # BUTTON FRAME
        # =================================================

        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # RETRY BUTTON
        # =================================================

        self.retry_button = ctk.CTkButton(

            self.button_frame,

            text="Retry",

            width=70,

            command=lambda:
            retry_callback(self.image_path)
        )

        self.retry_button.pack(
            side="right",
            padx=5
        )

        # =================================================
        # CANCEL BUTTON
        # =================================================

        self.cancel_button = ctk.CTkButton(

            self.button_frame,

            text="Cancel",

            width=70,

            command=lambda:
            cancel_callback(self.image_path)
        )

        self.cancel_button.pack(
            side="right",
            padx=5
        )

        # =================================================
        # REMOVE BUTTON
        # =================================================

        self.remove_button = ctk.CTkButton(

            self.button_frame,

            text="Remove",

            width=70,

            command=lambda:
            remove_callback(self.image_path)
        )

        self.remove_button.pack(
            side="right",
            padx=5
        )

        # =================================================
        # INITIAL UPDATE
        # =================================================

        self.update_item()

    # =====================================================
    # UPDATE ITEM
    # =====================================================

    def update_item(
        self
    ):

        status = app_state.task_status.get(
            self.image_path,
            "waiting"
        )

        progress = app_state.task_progress.get(
            self.image_path,
            0
        )

        start_time = app_state.task_start_time.get(
            self.image_path
        )

        filename = os.path.basename(
            self.image_path
        )

        # =================================================
        # ETA
        # =================================================

        eta_text = ""

        if (
            status == "processing" and
            start_time and
            progress > 0
        ):

            elapsed = (
                time.time() - start_time
            )

            estimated_total = (
                elapsed / (progress / 100)
            )

            remaining = max(
                0,
                estimated_total - elapsed
            )

            eta_text = (
                f" • ETA {remaining:.1f}s"
            )

        # =================================================
        # STATUS ICON
        # =================================================

        icon = "🕒"

        if status == "processing":

            icon = "⏳"

        elif status == "done":

            icon = "✅"

        elif status == "failed":

            icon = "❌"

        elif status == "cancelled":

            icon = "🛑"

        # =================================================
        # STATUS COLOR
        # =================================================

        status_color = "#888888"

        if status == "waiting":

            status_color = "#E6A700"

        elif status == "processing":

            status_color = "#3B82F6"

        elif status == "done":

            status_color = "#22C55E"

        elif status == "failed":

            status_color = "#EF4444"

        elif status == "cancelled":

            status_color = "#6B7280"

        # =================================================
        # UPDATE LABEL
        # =================================================

        self.label.configure(

            text=(
                f"{icon} "
                f"[{status.upper()}] "
                f"{filename}"
                f"{eta_text}"
            ),

            text_color=status_color
        )

        # =================================================
        # UPDATE PROGRESS
        # =================================================

        self.progressbar.set(
            progress / 100
        )