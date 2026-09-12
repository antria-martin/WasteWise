from typing import Dict, Any
from app.config import CONFIDENCE_THRESHOLD


def verify_predictions(
    predicted_object: str,
    predicted_category: str,
    confidence: float,
    threshold: float = CONFIDENCE_THRESHOLD,
) -> Dict[str, Any]:
    """
    Verifies that the single-model confidence meets the threshold.

    Because the model already encodes a fixed (object, category) pairing per class,
    there is no longer a separate compatibility check between two independent heads.

    Returns a standardised response dict consumed by the /predict route.
    """
    if confidence < threshold:
        return {
            "identifiable":       False,
            "object":             None,
            "category":           None,
            "confidence":         round(confidence, 4),
            "message": (
                "The item could not be identified confidently. "
                "Please upload a clearer image or ensure the image contains a waste item."
            ),
        }

    return {
        "identifiable": True,
        "object":       predicted_object,
        "category":     predicted_category,
        "confidence":   round(confidence, 4),
        "message":      "Item successfully identified.",
    }
