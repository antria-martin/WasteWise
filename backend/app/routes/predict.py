import time
import torch
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Optional

from app.preprocessing.image import preprocess_image
from app.mappings.compatibility import verify_predictions
from app.inference.waste_classifier import WasteClassifier

router = APIRouter()

# Single global classifier instance (initialised during FastAPI lifespan)
waste_classifier: Optional[WasteClassifier] = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def init_services():
    global waste_classifier
    if waste_classifier is None:
        waste_classifier = WasteClassifier()


@router.post("/predict")
async def predict_waste_item(
    image: UploadFile = File(...),
):
    """
    Waste identification endpoint.

    Accepts a multipart/form-data image upload.
    Runs preprocessing (exact training transforms from inference_bundle.json),
    single PyTorch model inference, and confidence verification.

    Returns identified object + waste category with top-k confidence breakdown.
    """
    init_services()

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        contents = await image.read()
        t0 = time.time()

        # 1. Preprocess — mirrors training transforms exactly
        tensor, b64_preview = preprocess_image(contents, device=_device)

        # 2. Single-model inference
        result = waste_classifier.predict(tensor, top_k=3)
        cv_latency_ms = round((time.time() - t0) * 1000, 2)

        # 3. Confidence threshold verification
        verification = verify_predictions(
            predicted_object=result["object"],
            predicted_category=result["category"],
            confidence=result["confidence"],
        )

        return {
            **verification,
            "top_k_predictions":  result["top_k_predictions"],
            "latency": {
                "cv_latency_ms": cv_latency_ms,
            },
            "preprocessed_preview": b64_preview,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
