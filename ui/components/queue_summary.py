import customtkinter as ctk

from core.app_state import (
    app_state
)


# =========================================================
# QUEUE SUMMARY
# =========================================================

class QueueSummary(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(parent)

        # =================================================
        # LAYOUT
        # =================================================

        self.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # SUMMARY LABEL
        # =================================================

        self.summary_label = ctk.CTkLabel(
            self,
            text="0 / 0 completed"
        )

        self.summary_label.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =================================================
        # SUMMARY PROGRESSBAR
        # =================================================

        self.summary_progressbar = (
            ctk.CTkProgressBar(
                self,
                height=14
            )
        )

        self.summary_progressbar.pack(
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        self.summary_progressbar.set(0)

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(
        self
    ):

        total_tasks = len(
            app_state.image_paths
        )

        completed = 0

        for path in app_state.image_paths:

            status = app_state.task_status.get(
                path
            )

            if status in [
                "done",
                "failed",
                "cancelled"
            ]:

                completed += 1

        # =================================================
        # PERCENT
        # =================================================

        progress = 0

        if total_tasks > 0:

            progress = (
                completed / total_tasks
            )

        # =================================================
        # UPDATE UI
        # =================================================

        self.summary_label.configure(
            text=(
                f"{completed} / "
                f"{total_tasks} completed"
            )
        )

        self.summary_progressbar.set(
            progress
        )