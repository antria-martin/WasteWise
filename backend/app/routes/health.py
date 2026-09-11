from fastapi import APIRouter
from app.config import CONFIDENCE_THRESHOLD, OBJECT_MODEL_PATH, CATEGORY_MODEL_PATH

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "WasteWise AI Backend",
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "models": {
            "object_model_present": OBJECT_MODEL_PATH.exists(),
            "category_model_present": CATEGORY_MODEL_PATH.exists()
        }
    }
