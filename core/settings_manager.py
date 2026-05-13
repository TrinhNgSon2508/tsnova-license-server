# core/settings_manager.py

import json
import os


# =========================================================
# SETTINGS FILE
# =========================================================

SETTINGS_FILE = "settings.json"


# =========================================================
# DEFAULT SETTINGS
# =========================================================

DEFAULT_SETTINGS = {

    # =====================================================
    # AI
    # =====================================================

    "current_model": "RealESRGAN_x2",

    "gpu_enabled": True,

    "tile_size": 0,

    # =====================================================
    # WORKERS
    # =====================================================

    "max_workers": 4,

    "auto_retry": True,

    "retry_limit": 2,

    # =====================================================
    # OUTPUT
    # =====================================================

    "output_folder": "",

    "overwrite_existing": False,

    "save_format": "auto",

    # =====================================================
    # UI
    # =====================================================

    "theme": "dark",

    "show_progress": True,

    "show_performance_panel": True,

    # =====================================================
    # PERFORMANCE
    # =====================================================

    "thumbnail_cache_limit": 500,

    "lazy_rendering": True,

    "virtualization_enabled": True
}


# =========================================================
# SETTINGS MANAGER
# =========================================================

class SettingsManager:

    def __init__(self):

        self.settings = (
            DEFAULT_SETTINGS.copy()
        )

        self.load_settings()

    # =====================================================
    # LOAD SETTINGS
    # =====================================================

    def load_settings(self):

        try:

            # =============================================
            # FILE NOT EXISTS
            # =============================================

            if not os.path.exists(
                SETTINGS_FILE
            ):

                self.save_settings()

                return

            # =============================================
            # LOAD JSON
            # =============================================

            with open(

                SETTINGS_FILE,

                "r",

                encoding="utf-8"

            ) as file:

                data = json.load(
                    file
                )

            # =============================================
            # MERGE
            # =============================================

            self.settings.update(
                data
            )

            print(
                "Settings loaded"
            )

        except Exception as error:

            print(
                f"Load Settings Error: {error}"
            )

    # =====================================================
    # SAVE SETTINGS
    # =====================================================

    def save_settings(self):

        try:

            with open(

                SETTINGS_FILE,

                "w",

                encoding="utf-8"

            ) as file:

                json.dump(

                    self.settings,

                    file,

                    indent=4
                )

            print(
                "Settings saved"
            )

            return True

        except Exception as error:

            print(
                f"Save Settings Error: {error}"
            )

            return False

    # =====================================================
    # GET SETTING
    # =====================================================

    def get(
        self,
        key,
        default=None
    ):

        return self.settings.get(
            key,
            default
        )

    # =====================================================
    # SET SETTING
    # =====================================================

    def set(
        self,
        key,
        value,
        auto_save=True
    ):

        self.settings[key] = value

        if auto_save:

            self.save_settings()

    # =====================================================
    # RESET SETTINGS
    # =====================================================

    def reset_settings(self):

        self.settings = (
            DEFAULT_SETTINGS.copy()
        )

        self.save_settings()

    # =====================================================
    # EXPORT SETTINGS
    # =====================================================

    def export_settings(self):

        return self.settings.copy()

    # =====================================================
    # IMPORT SETTINGS
    # =====================================================

    def import_settings(
        self,
        data
    ):

        try:

            if not isinstance(
                data,
                dict
            ):

                return False

            self.settings.update(
                data
            )

            self.save_settings()

            return True

        except Exception as error:

            print(
                f"Import Settings Error: {error}"
            )

            return False

    # =====================================================
    # APPLY SETTINGS
    # =====================================================

    def apply_settings(self):

        try:

            # =============================================
            # WORKERS
            # =============================================

            from core.app_state import (
                app_state
            )

            app_state.max_workers = self.get(
                "max_workers",
                4
            )

            # =============================================
            # MODEL
            # =============================================

            from services.ai.model_manager import (
                model_manager
            )

            model_manager.set_current_model(

                self.get(
                    "current_model",
                    "RealESRGAN_x2"
                )
            )

            print(
                "Settings applied"
            )

        except Exception as error:

            print(
                f"Apply Settings Error: {error}"
            )


# =========================================================
# GLOBAL INSTANCE
# =========================================================

settings_manager = SettingsManager()