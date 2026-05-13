import customtkinter as ctk


# =========================================================
# TOP TOOLBAR
# =========================================================

class TopToolbar(ctk.CTkFrame):

    def __init__(

        self,

        parent,

        pause_callback,

        resume_callback,

        clear_callback,

        add_files_callback=None,

        add_folder_callback=None,

        settings_callback=None,

        theme_callback=None
    ):

        super().__init__(parent)

        # =================================================
        # ADD FILES
        # =================================================

        self.add_files_button = ctk.CTkButton(

            self,

            text="Add Files",

            command=add_files_callback
        )

        self.add_files_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        # =================================================
        # ADD FOLDER
        # =================================================

        self.add_folder_button = ctk.CTkButton(

            self,

            text="Add Folder",

            command=add_folder_callback
        )

        self.add_folder_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        # =================================================
        # PAUSE
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
        # RESUME
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
        # SETTINGS
        # =================================================

        self.settings_button = ctk.CTkButton(

            self,

            text="Settings",

            command=settings_callback
        )

        self.settings_button.pack(
            side="right",
            padx=5,
            pady=5
        )

        # =================================================
        # THEME
        # =================================================

        self.theme_button = ctk.CTkButton(

            self,

            text="Theme",

            command=theme_callback
        )

        self.theme_button.pack(
            side="right",
            padx=5,
            pady=5
        )

        # =================================================
        # CLEAR
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