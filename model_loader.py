# model_loader.py

import torch

from transformers import (
    AutoModelForImageSegmentation
)

# =========================
# DEVICE
# =========================

device = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

# =========================
# LOAD MODEL
# =========================

def load_model(model_name):

    print(f"Loading {model_name}...")

    model = AutoModelForImageSegmentation.from_pretrained(
        model_name,
        trust_remote_code=True
    )

    model.to(device)

    model.eval()

    # FP16 for CUDA
    if device == "cuda":

        model.half()

    print(f"{model_name} loaded!")

    return model


# =========================
# FAST MODEL
# =========================

def load_fast_model():

    return load_model(
        "ZhengPeng7/BiRefNet"
    )


# =========================
# HD MODEL
# =========================

def load_hd_model():

    return load_model(
        "ZhengPeng7/BiRefNet-portrait"
    )