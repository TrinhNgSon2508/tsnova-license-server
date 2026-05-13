import customtkinter as ctk

from core.app_state import app_state

from ui.queue_item import QueueItem
from ui.preset_bar import PresetBar

from core.queue_sync import sync_queue_ui
from core.summary_updater import update_summary
from core.monitor_updater import update_monitor

from core.task_manager import (
    remove_task,
    retry_task,
    clear_completed_tasks
)


# =========================================================
# QUEUE PANEL
# =========================================================

class QueuePanel(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent
        )

        self.queue_items = {}

        self.build_ui()

        self.refresh()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # =================================================
        # TOP BAR
        # =================================================

        self.top_frame = ctk.CTkFrame(
            self
        )

        self.top_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10, 5)
        )

        self.top_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # =================================================
        # PRESET BAR
        # =================================================

        self.preset_bar = PresetBar(
            self.top_frame,
            self.on_preset_selected
        )

        self.preset_bar.grid(
            row=0,
            column=0,
            sticky="w"
        )

        # =================================================
        # CLEAR BUTTON
        # =================================================

        self.clear_button = ctk.CTkButton(
            self.top_frame,
            text="Clear Completed",
            command=self.clear_completed
        )

        self.clear_button.grid(
            row=0,
            column=2,
            padx=(10, 0)
        )

        # =================================================
        # SCROLL FRAME
        # =================================================

        self.scroll_frame = ctk.CTkScrollableFrame(
            self
        )

        self.scroll_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        self.scroll_frame.grid_columnconfigure(
            0,
            weight=1
        )

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        sync_queue_ui(
            queue_panel=self
        )

        update_summary()

        update_monitor()

        self.after(
            1000,
            self.refresh
        )

    # =====================================================
    # ADD ITEM
    # =====================================================

    def add_queue_item(
        self,
        task
    ):

        task_id = task["id"]

        if task_id in self.queue_items:
            return

        item = QueueItem(
            self.scroll_frame,
            task=task,
            remove_callback=self.remove_task,
            retry_callback=self.retry_task
        )

        item.pack(
            fill="x",
            padx=5,
            pady=5
        )

        self.queue_items[task_id] = item

    # =====================================================
    # UPDATE ITEM
    # =====================================================

    def update_queue_item(
        self,
        task
    ):

        task_id = task["id"]

        if task_id not in self.queue_items:
            return

        self.queue_items[task_id].update_task(
            task
        )

    # =====================================================
    # REMOVE ITEM
    # =====================================================

    def remove_queue_item(
        self,
        task_id
    ):

        if task_id not in self.queue_items:
            return

        item = self.queue_items.pop(
            task_id
        )

        item.destroy()

    # =====================================================
    # REMOVE TASK
    # =====================================================

    def remove_task(
        self,
        task_id
    ):

        remove_task(
            task_id
        )

    # =====================================================
    # RETRY TASK
    # =====================================================

    def retry_task(
        self,
        task_id
    ):

        retry_task(
            task_id
        )

    # =====================================================
    # CLEAR COMPLETED
    # =====================================================

    def clear_completed(self):

        clear_completed_tasks()

    # =====================================================
    # PRESET
    # =====================================================

    def on_preset_selected(
        self,
        preset
    ):

        print(
            f"[Preset Selected] {preset}"
        )
        # =====================================================
    # REFRESH QUEUE
    # =====================================================

    def refresh_queue(self):

        self.refresh()