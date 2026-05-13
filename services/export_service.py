import os
import shutil

from core.app_state import (
    app_state
)


# =========================================================
# EXPORT IMAGE
# =========================================================

def export_image(
    input_path,
    output_path
):

    # =====================================================
    # CREATE OUTPUT FOLDER
    # =====================================================

    output_folder = os.path.dirname(
        output_path
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # =====================================================
    # EXPORT FILE
    # =====================================================

    shutil.copy(
        input_path,
        output_path
    )

    return output_path