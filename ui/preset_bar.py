import customtkinter as ctk


# =========================================================
# PRESET BAR
# =========================================================

class PresetBar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        callback
    ):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.callback = callback

        self.build_ui()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.label = ctk.CTkLabel(
            self,
            text="Preset:"
        )

        self.label.pack(
            side="left",
            padx=(0, 10)
        )

        # =================================================
        # PRESET SELECT
        # =================================================

        self.option_menu = ctk.CTkOptionMenu(
            self,
            values=[
                "Default",
                "Fast",
                "High Quality",
                "AI Enhance"
            ],
            command=self.on_select
        )

        self.option_menu.pack(
            side="left"
        )

    # =====================================================
    # SELECT
    # =====================================================

    def on_select(
        self,
        value
    ):

        if self.callback:

            self.callback(
                value
            )