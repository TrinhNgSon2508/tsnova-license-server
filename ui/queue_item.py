import customtkinter as ctk


# =========================================================
# QUEUE ITEM
# =========================================================

class QueueItem(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        task,
        remove_callback,
        retry_callback
    ):

        super().__init__(
            parent
        )

        self.task = task

        self.remove_callback = remove_callback

        self.retry_callback = retry_callback

        self.build_ui()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.grid_columnconfigure(
            1,
            weight=1
        )

        # =================================================
        # FILE NAME
        # =================================================

        self.name_label = ctk.CTkLabel(
            self,
            text=self.task.get(
                "name",
                "Unknown"
            ),
            anchor="w"
        )

        self.name_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 0)
        )

        # =================================================
        # STATUS
        # =================================================

        self.status_label = ctk.CTkLabel(
            self,
            text=self.task.get(
                "status",
                "Waiting"
            )
        )

        self.status_label.grid(
            row=1,
            column=0,
            sticky="w",
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

        self.button_frame.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=10
        )

        # =================================================
        # RETRY BUTTON
        # =================================================

        self.retry_button = ctk.CTkButton(
            self.button_frame,
            text="Retry",
            width=70,
            command=self.on_retry
        )

        self.retry_button.pack(
            side="left",
            padx=5
        )

        # =================================================
        # REMOVE BUTTON
        # =================================================

        self.remove_button = ctk.CTkButton(
            self.button_frame,
            text="Remove",
            width=70,
            command=self.on_remove
        )

        self.remove_button.pack(
            side="left",
            padx=5
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update_task(
        self,
        task
    ):

        self.task = task

        self.name_label.configure(
            text=task.get(
                "name",
                "Unknown"
            )
        )

        self.status_label.configure(
            text=task.get(
                "status",
                "Waiting"
            )
        )

    # =====================================================
    # REMOVE
    # =====================================================

    def on_remove(self):

        self.remove_callback(
            self.task["id"]
        )

    # =====================================================
    # RETRY
    # =====================================================

    def on_retry(self):

        self.retry_callback(
            self.task["id"]
        )