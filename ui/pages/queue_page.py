import customtkinter as ctk


class QueuePage(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent
        )

        # =================================================
        # TITLE
        # =================================================

        title = ctk.CTkLabel(

            self,

            text="Queue",

            font=(
                "Arial",
                26,
                "bold"
            )
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # =================================================
        # STATS
        # =================================================

        self.stats_frame = (
            ctk.CTkFrame(
                self,
                height=100
            )
        )

        self.stats_frame.pack(

            fill="x",

            padx=20,
            pady=10
        )

        self.stats_frame.pack_propagate(
            False
        )

        self.queue_label = (
            ctk.CTkLabel(

                self.stats_frame,

                text="Waiting: 0",

                font=(
                    "Arial",
                    18
                )
            )
        )

        self.queue_label.pack(

            anchor="w",

            padx=20,
            pady=(20, 5)
        )

        self.processing_label = (
            ctk.CTkLabel(

                self.stats_frame,

                text="Processing: 0",

                font=(
                    "Arial",
                    18
                )
            )
        )

        self.processing_label.pack(

            anchor="w",

            padx=20
        )

        # =================================================
        # TASK LIST
        # =================================================

        self.task_scroll = (
            ctk.CTkScrollableFrame(
                self
            )
        )

        self.task_scroll.pack(

            fill="both",
            expand=True,

            padx=20,
            pady=(10, 20)
        )