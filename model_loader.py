import torch
from transformers import AutoModelForImageSegmentation

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading BiRefNet...")

model = AutoModelForImageSegmentation.from_pretrained(
    "ZhengPeng7/BiRefNet",
    trust_remote_code=True
)

model.to(device)
model.eval()

print("BiRefNet loaded!")