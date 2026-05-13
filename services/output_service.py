import os


# =========================================================
# OUTPUT SERVICE
# =========================================================

class OutputService:

    def __init__(self):

        self.output_dir = "outputs"

        self.output_map = {}

        self.ensure_output_dir()

    # =====================================================
    # OUTPUT PATH
    # =====================================================

    def get_output_path(
        self,
        input_path,
        suffix="_processed",
        extension=".png"
    ):

        filename = os.path.basename(
            input_path
        )

        name = os.path.splitext(
            filename
        )[0]

        output_filename = (
            f"{name}{suffix}{extension}"
        )

        output_path = os.path.join(
            self.output_dir,
            output_filename
        )

        # =============================================
        # SAVE MAP
        # =============================================

        self.output_map[
            input_path
        ] = output_path

        return output_path

    # =====================================================
    # GET PROCESSED PATH
    # =====================================================

    def get_processed_path(
        self,
        input_path
    ):

        return self.output_map.get(
            input_path
        )

    # =====================================================
    # SET OUTPUT DIR
    # =====================================================

    def set_output_dir(
        self,
        path
    ):

        self.output_dir = path

        self.ensure_output_dir()

    # =====================================================
    # ENSURE OUTPUT DIR
    # =====================================================

    def ensure_output_dir(self):

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )


# =========================================================
# GLOBAL INSTANCE
# =========================================================

output_service = OutputService()