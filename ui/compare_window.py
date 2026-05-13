import customtkinter as ctk

from ui.compare_slider import (
    CompareSlider
)


# =========================================================
# COMPARE WINDOW
# =========================================================

class CompareWindow(ctk.CTkToplevel):

    def __init__(
        self,
        original_path,
        processed_path
    ):

        super().__init__()

        # =================================================
        # WINDOW
        # =================================================

        self.title(
            "TSNOVA Compare Viewer"
        )

        self.geometry(
            "1100x760"
        )

        self.minsize(
            900,
            700
        )

        # =================================================
        # HEADER
        # =================================================

        self.header_label = ctk.CTkLabel(

            self,

            text="Before / After Compare",

            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.header_label.pack(
            pady=(20, 10)
        )

        # =================================================
        # SLIDER
        # =================================================

        self.compare_slider = CompareSlider(

            self,

            before_path=original_path,

            after_path=processed_path,

            width=1000,

            height=650
        )

        self.compare_slider.pack(
            padx=20,
            pady=20,
            expand=True
        )

        # =================================================
        # FOCUS
        # =================================================

        self.focus()

        self.grab_set()