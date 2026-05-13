import gc

from core.app_state import (
    app_state
)


# =========================================================
# CLEAR IMAGE CACHE
# =========================================================

def clear_image_cache():

    if hasattr(
        app_state,
        "preview_cache"
    ):

        app_state.preview_cache.clear()


# =========================================================
# CLEAR TEMP DATA
# =========================================================

def clear_temp_data():

    if hasattr(
        app_state,
        "temp_images"
    ):

        app_state.temp_images.clear()


# =========================================================
# FORCE GARBAGE COLLECTION
# =========================================================

def force_memory_cleanup():

    gc.collect()

    # =====================================================
    # TORCH CUDA
    # =====================================================

    try:

        import torch

        if torch.cuda.is_available():

            torch.cuda.empty_cache()

    except Exception:

        pass


# =========================================================
# FULL CLEANUP
# =========================================================

def full_memory_cleanup():

    clear_image_cache()

    clear_temp_data()

    force_memory_cleanup()