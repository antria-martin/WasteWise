import io
import json
import base64
import torch
from PIL import Image
from torchvision import transforms
from typing import Tuple

from app.config import INFERENCE_BUNDLE_PATH


def _load_bundle() -> dict:
    """Load the inference bundle JSON that was saved during training."""
    if not INFERENCE_BUNDLE_PATH.exists():
        raise FileNotFoundError(
            f"inference_bundle.json not found at {INFERENCE_BUNDLE_PATH}. "
            "Export it from your training notebook and place it in backend/app/models/."
        )
    with open(INFERENCE_BUNDLE_PATH, "r") as f:
        return json.load(f)


# Build the preprocessing pipeline once at import time (mirrors training exactly)
_bundle = _load_bundle()

preprocess = transforms.Compose([
    transforms.Resize(int(_bundle["img_size"] * 1.14)),
    transforms.CenterCrop(_bundle["img_size"]),
    transforms.ToTensor(),
    transforms.Normalize(_bundle["mean"], _bundle["std"]),
])


def preprocess_image(
    image_bytes: bytes,
    device: torch.device = torch.device("cpu"),
) -> Tuple[torch.Tensor, str]:
    """
    Preprocesses raw image bytes using the exact transform pipeline from training.

    Args:
        image_bytes: Raw bytes of the uploaded image file.
        device:      Torch device to place the tensor on.

    Returns:
        tensor:      Float32 tensor of shape (1, C, H, W), ready for model input.
        b64_preview: Base64 JPEG string of the cropped/resized image for UI display.
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # handles RGBA/grayscale/palette

    # Apply training-matched transforms
    tensor = preprocess(img).unsqueeze(0).to(device)  # (1, C, H, W)

    # Generate a preview image from the CenterCrop step (before normalization)
    preview_transform = transforms.Compose([
        transforms.Resize(int(_bundle["img_size"] * 1.14)),
        transforms.CenterCrop(_bundle["img_size"]),
    ])
    preview_img = preview_transform(img)

    buffer = io.BytesIO()
    preview_img.save(buffer, format="JPEG", quality=85)
    b64_preview = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return tensor, f"data:image/jpeg;base64,{b64_preview}"
