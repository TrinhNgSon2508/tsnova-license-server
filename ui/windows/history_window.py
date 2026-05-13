# ui/windows/history_window.py

import os

import customtkinter as ctk

from core.database import (
    database_manager
)

from core.app_state import (
    app_state
)

from ui.preview_manager import (
    preview_manager
)


class HistoryWindow(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        # =================================================
        # WINDOW
        # =================================================

        self.title(
            "TSNOVA History"
        )

        self.geometry(
            "1200x700"
        )

        self.minsize(
            900,
            600
        )

        # =================================================
        # STATE
        # =================================================

        self.current_filter = "all"

        self.search_text = ""

        # =================================================
        # UI
        # =================================================

        self.build_ui()

        self.load_tasks()

    # =====================================================
    # BUILD UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # TOPBAR
        # =================================================

        self.topbar = ctk.CTkFrame(
            self,
            height=70
        )

        self.topbar.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.topbar.pack_propagate(False)

        # =================================================
        # TITLE
        # =================================================

        title = ctk.CTkLabel(

            self.topbar,

            text="Task History",

            font=("Arial", 28, "bold")
        )

        title.pack(
            side="left",
            padx=20
        )

        # =================================================
        # SEARCH
        # =================================================

        self.search_entry = ctk.CTkEntry(

            self.topbar,

            placeholder_text="Search..."
        )

        self.search_entry.pack(

            side="left",

            padx=10,

            fill="x",

            expand=True
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.on_search
        )

        # =================================================
        # FILTER
        # =================================================

        self.filter_dropdown = (
            ctk.CTkOptionMenu(

                self.topbar,

                values=[
                    "all",
                    "waiting",
                    "processing",
                    "completed",
                    "failed",
                    "cancelled"
                ],

                command=self.on_filter_change
            )
        )

        self.filter_dropdown.pack(
            side="left",
            padx=10
        )

        # =================================================
        # REFRESH
        # =================================================

        refresh_button = ctk.CTkButton(

            self.topbar,

            text="Refresh",

            width=100,

            command=self.load_tasks
        )

        refresh_button.pack(
            side="right",
            padx=10
        )

        # =================================================
        # CLEAR HISTORY
        # =================================================

        clear_button = ctk.CTkButton(

            self.topbar,

            text="Clear History",

            fg_color="#cc4444",

            width=140,

            command=self.clear_history
        )

        clear_button.pack(
            side="right",
            padx=10
        )

        # =================================================
        # TASK LIST
        # =================================================

        self.task_container = (
            ctk.CTkScrollableFrame(
                self
            )
        )

        self.task_container.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=(0, 10)
        )

    # =====================================================
    # LOAD TASKS
    # =====================================================

    def load_tasks(self):

        for widget in (
            self.task_container.winfo_children()
        ):

            widget.destroy()

        tasks = (
            database_manager.get_all_tasks()
        )

        for task in tasks:

            # =============================================
            # FILTER
            # =============================================

            status = task["status"]

            if (
                self.current_filter != "all"

                and

                status != self.current_filter
            ):

                continue

            # =============================================
            # SEARCH
            # =============================================

            input_path = task[
                "input_path"
            ]

            filename = os.path.basename(
                input_path
            )

            if (

                self.search_text

                and

                self.search_text.lower()

                not in filename.lower()
            ):

                continue

            self.create_task_card(
                task
            )

    # =====================================================
    # CREATE CARD
    # =====================================================

    def create_task_card(
        self,
        task
    ):

        card = ctk.CTkFrame(
            self.task_container
        )

        card.pack(

            fill="x",

            padx=10,

            pady=8
        )

        # =================================================
        # FILE
        # =================================================

        filename = os.path.basename(
            task["input_path"]
        )

        file_label = ctk.CTkLabel(

            card,

            text=filename,

            font=("Arial", 16, "bold"),

            anchor="w"
        )

        file_label.pack(

            anchor="w",

            padx=15,

            pady=(10, 5)
        )

        # =================================================
        # STATUS
        # =================================================

        status_text = (
            f"Status: {task['status']}"
        )

        status_label = ctk.CTkLabel(

            card,

            text=status_text,

            anchor="w"
        )

        status_label.pack(
            anchor="w",
            padx=15
        )

        # =================================================
        # MODEL
        # =================================================

        model_label = ctk.CTkLabel(

            card,

            text=(
                f"Model: "
                f"{task['model_name']}"
            ),

            anchor="w"
        )

        model_label.pack(
            anchor="w",
            padx=15
        )

        # =================================================
        # PROGRESS
        # =================================================

        progress_label = ctk.CTkLabel(

            card,

            text=(
                f"Progress: "
                f"{task['progress']}%"
            ),

            anchor="w"
        )

        progress_label.pack(
            anchor="w",
            padx=15
        )

        # =================================================
        # RETRIES
        # =================================================

        retry_label = ctk.CTkLabel(

            card,

            text=(
                f"Retries: "
                f"{task['retry_count']}"
            ),

            anchor="w"
        )

        retry_label.pack(
            anchor="w",
            padx=15
        )

        # =================================================
        # CREATED
        # =================================================

        created_label = ctk.CTkLabel(

            card,

            text=(
                f"Created: "
                f"{task['created_at']}"
            ),

            anchor="w"
        )

        created_label.pack(
            anchor="w",
            padx=15
        )

        # =================================================
        # BUTTONS
        # =================================================

        button_frame = ctk.CTkFrame(
            card
        )

        button_frame.pack(

            fill="x",

            padx=10,

            pady=10
        )

        # =================================================
        # RETRY
        # =================================================

        retry_button = ctk.CTkButton(

            button_frame,

            text="Retry",

            width=100,

            command=lambda:
            self.retry_task(task)
        )

        retry_button.pack(
            side="left",
            padx=5
        )

        # =================================================
        # OPEN
        # =================================================

        open_button = ctk.CTkButton(

            button_frame,

            text="Open",

            width=100,

            command=lambda:
            self.open_task(task)
        )

        open_button.pack(
            side="left",
            padx=5
        )

        # =================================================
        # DELETE
        # =================================================

        delete_button = ctk.CTkButton(

            button_frame,

            text="Delete",

            width=100,

            fg_color="#cc4444",

            command=lambda:
            self.delete_task(task)
        )

        delete_button.pack(
            side="right",
            padx=5
        )

    # =====================================================
    # RETRY TASK
    # =====================================================

    def retry_task(
        self,
        task
    ):

        input_path = task[
            "input_path"
        ]

        if input_path not in app_state.image_paths:

            app_state.image_paths.append(
                input_path
            )

        app_state.processing_queue.put(
            input_path
        )

        app_state.task_status[
            input_path
        ] = "waiting"

        database_manager.increment_retry_count(
            input_path
        )

        database_manager.update_task_status(
            input_path,
            "waiting"
        )

        print(
            f"Retry queued: {input_path}"
        )

    # =====================================================
    # OPEN TASK
    # =====================================================

    def open_task(
        self,
        task
    ):

        path = task["input_path"]

        if os.path.exists(path):

            os.startfile(path)

    # =====================================================
    # DELETE TASK
    # =====================================================

    def delete_task(
        self,
        task
    ):

        database_manager.delete_task(
            task["input_path"]
        )

        self.load_tasks()

    # =====================================================
    # CLEAR HISTORY
    # =====================================================

    def clear_history(self):

        database_manager.clear_tasks()

        self.load_tasks()

    # =====================================================
    # SEARCH
    # =====================================================

    def on_search(
        self,
        event=None
    ):

        self.search_text = (
            self.search_entry.get()
        )

        self.load_tasks()

    # =====================================================
    # FILTER
    # =====================================================

    def on_filter_change(
        self,
        value
    ):

        self.current_filter = value

        self.load_tasks()