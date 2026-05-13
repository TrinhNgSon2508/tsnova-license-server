import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

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

            text="Settings",

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
        # SETTINGS FRAME
        # =================================================

        settings_frame = (
            ctk.CTkFrame(
                self
            )
        )

        settings_frame.pack(

            fill="x",

            padx=20,
            pady=10
        )

        # =================================================
        # OUTPUT FORMAT
        # =================================================

        format_label = (
            ctk.CTkLabel(

                settings_frame,

                text="Output Format",

                font=(
                    "Arial",
                    18
                )
            )
        )

        format_label.pack(

            anchor="w",

            padx=20,
            pady=(20, 5)
        )

        self.format_option = (
            ctk.CTkOptionMenu(

                settings_frame,

                values=[
                    "PNG",
                    "JPG",
                    "WEBP"
                ]
            )
        )

        self.format_option.pack(

            anchor="w",

            padx=20,
            pady=(0, 20)
        )

        # =================================================
        # AI MODEL
        # =================================================

        model_label = (
            ctk.CTkLabel(

                settings_frame,

                text="AI Model",

                font=(
                    "Arial",
                    18
                )
            )
        )

        model_label.pack(

            anchor="w",

            padx=20,
            pady=(0, 5)
        )

        self.model_option = (
            ctk.CTkOptionMenu(

                settings_frame,

                values=[
                    "RealESRGAN",
                    "SwinIR",
                    "AnimeSharp"
                ]
            )
        )

        self.model_option.pack(

            anchor="w",

            padx=20,
            pady=(0, 20)
        )