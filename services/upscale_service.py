import os

from services.ai.realesrgan_engine import (
    realesrgan_engine
)


# =========================================================
# CONFIG
# =========================================================

DEFAULT_MODEL = "RealESRGAN_x2"


# =========================================================
# ENSURE MODEL
# =========================================================

def ensure_model_loaded():

    if realesrgan_engine.model_loaded:
        return True

    return realesrgan_engine.load_model(
        DEFAULT_MODEL
    )


# =========================================================
# BUILD OUTPUT PATH
# =========================================================

def build_output_path(
    input_path
):

    directory = os.path.dirname(
        input_path
    )

    filename = os.path.basename(
        input_path
    )

    name, extension = os.path.splitext(
        filename
    )

    output_filename = (
        f"{name}_upscaled{extension}"
    )

    return os.path.join(
        directory,
        output_filename
    )


# =========================================================
# UPSCALE IMAGE
# =========================================================

def upscale_image(
    file_path,
    progress_callback=None
):

    try:

        # =================================================
        # VALIDATE FILE
        # =================================================

        if not os.path.exists(
            file_path
        ):

            print(
                f"Input file missing: {file_path}"
            )

            return False

        # =================================================
        # LOAD MODEL
        # =================================================

        model_ready = ensure_model_loaded()

        if not model_ready:

            print(
                "Failed to load AI model"
            )

            return False

        # =================================================
        # OUTPUT
        # =================================================

        output_path = build_output_path(
            file_path
        )

        # =================================================
        # UPSCALE
        # =================================================

        success = realesrgan_engine.upscale(

            input_path=file_path,

            output_path=output_path,

            progress_callback=progress_callback
        )

        # =================================================
        # RESULT
        # =================================================

        return success

    except Exception as error:

        print(
            f"Upscale Service Error: {error}"
        )

        return False