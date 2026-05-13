# services/ai/model_manager.py


# =========================================================
# MODEL REGISTRY
# =========================================================

MODELS = {

    # =====================================================
    # PHOTO MODELS
    # =====================================================

    "RealESRGAN_x2": {

        "display_name": "RealESRGAN x2",

        "scale": 2,

        "type": "photo",

        "engine": "realesrgan",

        "vram": 2,

        "tile_size": 0,

        "description": "Balanced photo upscale model"
    },

    "RealESRGAN_x4": {

        "display_name": "RealESRGAN x4",

        "scale": 4,

        "type": "photo",

        "engine": "realesrgan",

        "vram": 4,

        "tile_size": 0,

        "description": "High quality photo upscale"
    },

    # =====================================================
    # ANIME MODELS
    # =====================================================

    "Anime_x4": {

        "display_name": "Anime x4",

        "scale": 4,

        "type": "anime",

        "engine": "realesrgan",

        "vram": 3,

        "tile_size": 0,

        "description": "Anime optimized upscale"
    },

    # =====================================================
    # FAST MODELS
    # =====================================================

    "Fast_x2": {

        "display_name": "Fast x2",

        "scale": 2,

        "type": "fast",

        "engine": "realesrgan",

        "vram": 1,

        "tile_size": 0,

        "description": "Fast low VRAM upscale"
    }
}


# =========================================================
# MODEL MANAGER
# =========================================================

class ModelManager:

    def __init__(self):

        # =================================================
        # CURRENT MODEL
        # =================================================

        self.current_model = (
            "RealESRGAN_x2"
        )

    # =====================================================
    # GET MODEL
    # =====================================================

    def get_model(
        self,
        model_name
    ):

        return MODELS.get(
            model_name
        )

    # =====================================================
    # GET CURRENT MODEL
    # =====================================================

    def get_current_model(self):

        return self.get_model(
            self.current_model
        )

    # =====================================================
    # SET CURRENT MODEL
    # =====================================================

    def set_current_model(
        self,
        model_name
    ):

        if model_name not in MODELS:

            print(
                f"Unknown model: {model_name}"
            )

            return False

        self.current_model = model_name

        print(
            f"Current model set: {model_name}"
        )

        return True

    # =====================================================
    # GET CURRENT MODEL NAME
    # =====================================================

    def get_current_model_name(self):

        return self.current_model

    # =====================================================
    # GET ALL MODELS
    # =====================================================

    def get_all_models(self):

        return MODELS

    # =====================================================
    # GET MODEL LIST
    # =====================================================

    def get_model_names(self):

        return list(
            MODELS.keys()
        )

    # =====================================================
    # GET MODELS BY TYPE
    # =====================================================

    def get_models_by_type(
        self,
        model_type
    ):

        results = {}

        for model_name, data in MODELS.items():

            if data["type"] == model_type:

                results[model_name] = data

        return results

    # =====================================================
    # GET SCALE
    # =====================================================

    def get_scale(
        self,
        model_name=None
    ):

        if model_name is None:

            model_name = self.current_model

        model = self.get_model(
            model_name
        )

        if not model:
            return 2

        return model["scale"]

    # =====================================================
    # GET ENGINE
    # =====================================================

    def get_engine_name(
        self,
        model_name=None
    ):

        if model_name is None:

            model_name = self.current_model

        model = self.get_model(
            model_name
        )

        if not model:
            return None

        return model["engine"]

    # =====================================================
    # GET VRAM REQUIREMENT
    # =====================================================

    def get_vram_requirement(
        self,
        model_name=None
    ):

        if model_name is None:

            model_name = self.current_model

        model = self.get_model(
            model_name
        )

        if not model:
            return 0

        return model["vram"]

    # =====================================================
    # VALIDATE MODEL
    # =====================================================

    def validate_model(
        self,
        model_name
    ):

        return model_name in MODELS


# =========================================================
# GLOBAL INSTANCE
# =========================================================

model_manager = ModelManager()