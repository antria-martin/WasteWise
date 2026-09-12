from fastapi import APIRouter
from app.config import CONFIDENCE_THRESHOLD, MODEL_PATH, INFERENCE_BUNDLE_PATH

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "WasteWise AI Backend",
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "models": {
            "model_present": MODEL_PATH.exists(),
            "inference_bundle_present": INFERENCE_BUNDLE_PATH.exists(),
        }
    }
