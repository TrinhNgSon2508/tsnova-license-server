import customtkinter as ctk


# =========================================================
# CONTROL BAR
# =========================================================

class ControlBar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        pause_callback,
        resume_callback,
        clear_callback
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
        # PAUSE BUTTON
        # =================================================

        self.pause_button = ctk.CTkButton(

            self,

            text="Pause",

            command=pause_callback
        )

        self.pause_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        # =================================================
        # RESUME BUTTON
        # =================================================

        self.resume_button = ctk.CTkButton(

            self,

            text="Resume",

            command=resume_callback
        )

        self.resume_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        # =================================================
        # CLEAR BUTTON
        # =================================================

        self.clear_button = ctk.CTkButton(

            self,

            text="Clear Queue",

            command=clear_callback
        )

        self.clear_button.pack(
            side="right",
            padx=5,
            pady=5
        )