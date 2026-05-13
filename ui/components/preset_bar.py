import customtkinter as ctk

from core.preset_manager import (
    PRESETS
)


# =========================================================
# PRESET BAR
# =========================================================

class PresetBar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        callback
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
        # LABEL
        # =================================================

        self.label = ctk.CTkLabel(
            self,
            text="Preset"
        )

        self.label.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =================================================
        # OPTION MENU
        # =================================================

        self.option_menu = ctk.CTkOptionMenu(

            self,

            values=list(
                PRESETS.keys()
            ),

            command=callback
        )

        self.option_menu.pack(
            side="left",
            padx=10,
            pady=10
        )