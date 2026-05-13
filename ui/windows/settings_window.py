# ui/windows/settings_window.py

import customtkinter as ctk

from tkinter import filedialog

from core.settings_manager import (
    settings_manager
)

from services.ai.model_manager import (
    model_manager
)


class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        # =================================================
        # WINDOW
        # =================================================

        self.title(
            "TSNOVA Settings"
        )

        self.geometry(
            "620x700"
        )

        self.resizable(
            False,
            False
        )

        self.build_ui()

    # =====================================================
    # BUILD UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # TITLE
        # =================================================

        title_label = ctk.CTkLabel(

            self,

            text="TSNOVA Settings",

            font=("Arial", 28, "bold")
        )

        title_label.pack(
            pady=(20, 10)
        )

        # =================================================
        # SCROLL FRAME
        # =================================================

        self.scroll_frame = (
            ctk.CTkScrollableFrame(
                self
            )
        )

        self.scroll_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=10
        )

        # =================================================
        # AI SECTION
        # =================================================

        self.build_ai_section()

        # =================================================
        # WORKER SECTION
        # =================================================

        self.build_worker_section()

        # =================================================
        # OUTPUT SECTION
        # =================================================

        self.build_output_section()

        # =================================================
        # UI SECTION
        # =================================================

        self.build_ui_section()

        # =================================================
        # BUTTONS
        # =================================================

        self.build_bottom_buttons()

    # =====================================================
    # SECTION HEADER
    # =====================================================

    def create_section_title(
        self,
        text
    ):

        label = ctk.CTkLabel(

            self.scroll_frame,

            text=text,

            font=("Arial", 20, "bold")
        )

        label.pack(

            anchor="w",

            pady=(20, 10)
        )

    # =====================================================
    # AI SECTION
    # =====================================================

    def build_ai_section(self):

        self.create_section_title(
            "AI Settings"
        )

        # =================================================
        # MODEL
        # =================================================

        model_label = ctk.CTkLabel(

            self.scroll_frame,

            text="AI Model"
        )

        model_label.pack(
            anchor="w"
        )

        self.model_dropdown = (
            ctk.CTkOptionMenu(

                self.scroll_frame,

                values=model_manager.get_model_names()
            )
        )

        self.model_dropdown.pack(

            fill="x",

            pady=(5, 15)
        )

        self.model_dropdown.set(

            settings_manager.get(
                "current_model"
            )
        )

        # =================================================
        # GPU
        # =================================================

        self.gpu_switch = (
            ctk.CTkSwitch(

                self.scroll_frame,

                text="Enable GPU"
            )
        )

        self.gpu_switch.pack(
            anchor="w",
            pady=(0, 15)
        )

        if settings_manager.get(
            "gpu_enabled"
        ):

            self.gpu_switch.select()

        # =================================================
        # TILE SIZE
        # =================================================

        tile_label = ctk.CTkLabel(

            self.scroll_frame,

            text="Tile Size"
        )

        tile_label.pack(
            anchor="w"
        )

        self.tile_entry = (
            ctk.CTkEntry(
                self.scroll_frame
            )
        )

        self.tile_entry.pack(

            fill="x",

            pady=(5, 15)
        )

        self.tile_entry.insert(

            0,

            str(
                settings_manager.get(
                    "tile_size"
                )
            )
        )

    # =====================================================
    # WORKER SECTION
    # =====================================================

    def build_worker_section(self):

        self.create_section_title(
            "Worker Settings"
        )

        worker_label = ctk.CTkLabel(

            self.scroll_frame,

            text="Max Workers"
        )

        worker_label.pack(
            anchor="w"
        )

        self.worker_slider = (
            ctk.CTkSlider(

                self.scroll_frame,

                from_=1,

                to=16,

                number_of_steps=15
            )
        )

        self.worker_slider.pack(

            fill="x",

            pady=(5, 10)
        )

        self.worker_slider.set(

            settings_manager.get(
                "max_workers"
            )
        )

        self.worker_value_label = (
            ctk.CTkLabel(

                self.scroll_frame,

                text=f"{int(self.worker_slider.get())}"
            )
        )

        self.worker_value_label.pack(
            anchor="e"
        )

        self.worker_slider.configure(
            command=self.on_worker_change
        )

        # =================================================
        # AUTO RETRY
        # =================================================

        self.retry_switch = (
            ctk.CTkSwitch(

                self.scroll_frame,

                text="Enable Auto Retry"
            )
        )

        self.retry_switch.pack(
            anchor="w",
            pady=(10, 10)
        )

        if settings_manager.get(
            "auto_retry"
        ):

            self.retry_switch.select()

    # =====================================================
    # OUTPUT SECTION
    # =====================================================

    def build_output_section(self):

        self.create_section_title(
            "Output Settings"
        )

        output_label = ctk.CTkLabel(

            self.scroll_frame,

            text="Output Folder"
        )

        output_label.pack(
            anchor="w"
        )

        self.output_frame = (
            ctk.CTkFrame(
                self.scroll_frame
            )
        )

        self.output_frame.pack(

            fill="x",

            pady=(5, 15)
        )

        self.output_entry = (
            ctk.CTkEntry(
                self.output_frame
            )
        )

        self.output_entry.pack(

            side="left",

            fill="x",

            expand=True,

            padx=(0, 10)
        )

        self.output_entry.insert(

            0,

            settings_manager.get(
                "output_folder"
            )
        )

        browse_button = ctk.CTkButton(

            self.output_frame,

            text="Browse",

            width=100,

            command=self.select_output_folder
        )

        browse_button.pack(
            side="right"
        )

        # =================================================
        # OVERWRITE
        # =================================================

        self.overwrite_switch = (
            ctk.CTkSwitch(

                self.scroll_frame,

                text="Overwrite Existing Files"
            )
        )

        self.overwrite_switch.pack(
            anchor="w"
        )

        if settings_manager.get(
            "overwrite_existing"
        ):

            self.overwrite_switch.select()

    # =====================================================
    # UI SECTION
    # =====================================================

    def build_ui_section(self):

        self.create_section_title(
            "UI Settings"
        )

        # =================================================
        # THEME
        # =================================================

        theme_label = ctk.CTkLabel(

            self.scroll_frame,

            text="Theme"
        )

        theme_label.pack(
            anchor="w"
        )

        self.theme_dropdown = (
            ctk.CTkOptionMenu(

                self.scroll_frame,

                values=[
                    "dark",
                    "light"
                ]
            )
        )

        self.theme_dropdown.pack(

            fill="x",

            pady=(5, 15)
        )

        self.theme_dropdown.set(

            settings_manager.get(
                "theme"
            )
        )

        # =================================================
        # SHOW PERFORMANCE
        # =================================================

        self.performance_switch = (
            ctk.CTkSwitch(

                self.scroll_frame,

                text="Show Performance Panel"
            )
        )

        self.performance_switch.pack(
            anchor="w"
        )

        if settings_manager.get(
            "show_performance_panel"
        ):

            self.performance_switch.select()

    # =====================================================
    # BOTTOM BUTTONS
    # =====================================================

    def build_bottom_buttons(self):

        button_frame = ctk.CTkFrame(
            self
        )

        button_frame.pack(

            fill="x",

            padx=20,

            pady=15
        )

        save_button = ctk.CTkButton(

            button_frame,

            text="Save Settings",

            height=42,

            command=self.save_settings
        )

        save_button.pack(

            side="right",

            padx=(10, 0)
        )

        reset_button = ctk.CTkButton(

            button_frame,

            text="Reset",

            fg_color="#cc4444",

            height=42,

            command=self.reset_settings
        )

        reset_button.pack(
            side="right"
        )

    # =====================================================
    # WORKER SLIDER
    # =====================================================

    def on_worker_change(
        self,
        value
    ):

        self.worker_value_label.configure(
            text=f"{int(value)}"
        )

    # =====================================================
    # SELECT OUTPUT FOLDER
    # =====================================================

    def select_output_folder(self):

        folder = filedialog.askdirectory()

        if not folder:
            return

        self.output_entry.delete(
            0,
            "end"
        )

        self.output_entry.insert(
            0,
            folder
        )

    # =====================================================
    # SAVE SETTINGS
    # =====================================================

    def save_settings(self):

        settings_manager.set(

            "current_model",

            self.model_dropdown.get(),

            auto_save=False
        )

        settings_manager.set(

            "gpu_enabled",

            self.gpu_switch.get(),

            auto_save=False
        )

        settings_manager.set(

            "tile_size",

            int(
                self.tile_entry.get()
            ),

            auto_save=False
        )

        settings_manager.set(

            "max_workers",

            int(
                self.worker_slider.get()
            ),

            auto_save=False
        )

        settings_manager.set(

            "auto_retry",

            self.retry_switch.get(),

            auto_save=False
        )

        settings_manager.set(

            "output_folder",

            self.output_entry.get(),

            auto_save=False
        )

        settings_manager.set(

            "overwrite_existing",

            self.overwrite_switch.get(),

            auto_save=False
        )

        settings_manager.set(

            "theme",

            self.theme_dropdown.get(),

            auto_save=False
        )

        settings_manager.set(

            "show_performance_panel",

            self.performance_switch.get(),

            auto_save=False
        )

        settings_manager.save_settings()

        settings_manager.apply_settings()

        self.destroy()

    # =====================================================
    # RESET SETTINGS
    # =====================================================

    def reset_settings(self):

        settings_manager.reset_settings()

        self.destroy()