# services/ai/realesrgan_engine.py

import os
import threading

from PIL import Image


class RealESRGANEngine:

    def __init__(self):

        # =================================================
        # MODEL STATE
        # =================================================

        self.model = None

        self.model_name = None

        self.model_loaded = False

        # =================================================
        # ENGINE CONFIG
        # =================================================

        self.scale = 2

        self.tile_size = 0

        self.gpu_enabled = True

        # =================================================
        # THREAD LOCK
        # =================================================

        self.lock = threading.Lock()

    # =====================================================
    # LOAD MODEL
    # =====================================================

    def load_model(
        self,
        model_name="RealESRGAN_x2"
    ):

        with self.lock:

            try:

                # =========================================
                # ALREADY LOADED
                # =========================================

                if (
                    self.model_loaded and
                    self.model_name == model_name
                ):

                    return True

                # =========================================
                # UNLOAD OLD MODEL
                # =========================================

                self.unload_model()

                # =========================================
                # LOAD MODEL
                # =========================================

                print(
                    f"Loading model: {model_name}"
                )

                # =========================================
                # PLACEHOLDER
                # Replace with real model load later
                # =========================================

                self.model = "MODEL_PLACEHOLDER"

                self.model_name = model_name

                self.model_loaded = True

                print(
                    f"Model loaded: {model_name}"
                )

                return True

            except Exception as error:

                print(
                    f"Load Model Error: {error}"
                )

                self.model_loaded = False

                return False

    # =====================================================
    # UPSCALE
    # =====================================================

    def upscale(
        self,
        input_path,
        output_path=None,
        progress_callback=None
    ):

        with self.lock:

            try:

                # =========================================
                # CHECK MODEL
                # =========================================

                if not self.model_loaded:

                    success = self.load_model()

                    if not success:
                        return False

                # =========================================
                # VALIDATE INPUT
                # =========================================

                if not os.path.exists(
                    input_path
                ):

                    print(
                        f"File not found: {input_path}"
                    )

                    return False

                # =========================================
                # PROGRESS HELPER
                # =========================================

                def update_progress(value):

                    if progress_callback:

                        try:
                            progress_callback(value)
                        except:
                            pass

                # =========================================
                # LOAD IMAGE
                # =========================================

                update_progress(10)

                image = Image.open(
                    input_path
                ).convert("RGB")

                # =========================================
                # IMAGE SIZE
                # =========================================

                update_progress(25)

                width, height = image.size

                # =========================================
                # UPSCALE
                # =========================================

                update_progress(50)

                upscaled_image = image.resize(

                    (
                        width * self.scale,
                        height * self.scale
                    ),

                    Image.LANCZOS
                )

                # =========================================
                # OUTPUT PATH
                # =========================================

                update_progress(75)

                if output_path is None:

                    directory = os.path.dirname(
                        input_path
                    )

                    filename = os.path.basename(
                        input_path
                    )

                    name, extension = (
                        os.path.splitext(
                            filename
                        )
                    )

                    output_filename = (
                        f"{name}_upscaled{extension}"
                    )

                    output_path = os.path.join(
                        directory,
                        output_filename
                    )

                # =========================================
                # SAVE
                # =========================================

                update_progress(90)

                upscaled_image.save(
                    output_path
                )

                # =========================================
                # DONE
                # =========================================

                update_progress(100)

                return True

            except Exception as error:

                print(
                    f"Upscale Error: {error}"
                )

                return False

    # =====================================================
    # UNLOAD MODEL
    # =====================================================

    def unload_model(self):

        with self.lock:

            try:

                self.model = None

                self.model_name = None

                self.model_loaded = False

                print(
                    "Model unloaded"
                )

            except Exception as error:

                print(
                    f"Unload Model Error: {error}"
                )

    # =====================================================
    # GET INFO
    # =====================================================

    def get_engine_info(self):

        return {

            "model_loaded": self.model_loaded,

            "model_name": self.model_name,

            "scale": self.scale,

            "gpu_enabled": self.gpu_enabled,

            "tile_size": self.tile_size
        }


# =========================================================
# GLOBAL ENGINE
# =========================================================

realesrgan_engine = RealESRGANEngine()