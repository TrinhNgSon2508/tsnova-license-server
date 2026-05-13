import gc
import os

import torch

from PIL import Image

from core.logger import logger

from models.model_loader import (
    model_manager
)

from services.output_service import (
    output_service
)


# =========================================================
# RUN INFERENCE
# =========================================================

def run_inference(
    image,
    model
):

    # =====================================================
    # TEMP FAKE AI
    # =====================================================

    return image.copy()


# =========================================================
# MEMORY CLEANUP
# =========================================================

def cleanup_memory():

    gc.collect()

    if torch.cuda.is_available():

        torch.cuda.empty_cache()

        torch.cuda.ipc_collect()


# =========================================================
# PROCESS IMAGE
# =========================================================

def process_image(
    image_path
):

    try:

        logger.log(
            f"Opening image: {os.path.basename(image_path)}"
        )

        # =================================================
        # LOAD IMAGE
        # =================================================

        image = Image.open(
            image_path
        ).convert("RGBA")

        # =================================================
        # GET MODEL
        # =================================================

        model = model_manager.get_model()

        if model is None:

            logger.log(
                "No AI model loaded - fallback mode"
            )

            result = image.copy()

        else:

            # =============================================
            # INFERENCE
            # =============================================

            with torch.no_grad():

                result = run_inference(
                    image=image,
                    model=model
                )

        # =================================================
        # OUTPUT PATH
        # =================================================

        output_path = output_service.get_output_path(
            image_path
        )

        # =================================================
        # SAVE
        # =================================================

        result.save(
            output_path
        )

        logger.log(
            f"Saved output: {output_path}"
        )

        # =================================================
        # CLEANUP
        # =================================================

        del image

        del result

        cleanup_memory()

        return True

    except Exception as e:

        logger.log(
            f"Processing error: {e}"
        )

        cleanup_memory()

        return False