from typing import Dict, Set, Any
from app.config import CONFIDENCE_THRESHOLD

OBJECT_CATEGORY_COMPATIBILITY: Dict[str, Set[str]] = {
    "plastic_bottle": {"plastic"},
    "plastic_bag": {"plastic"},
    "plastic_container": {"plastic"},
    "plastic_cup": {"plastic"},
    
    "glass_bottle": {"glass"},
    "glass_jar": {"glass"},
    
    "metal_can": {"metal"},
    "metal_container": {"metal"},
    
    "cardboard_box": {"cardboard"},
    "newspaper": {"paper"},
    "paper_cup": {"paper"},
    
    "food_waste": {"organic"},
    
    "battery": {"hazardous"},
    "mobile_phone": {"e_waste", "hazardous"},
    "laptop": {"e_waste", "hazardous"},
    
    "general_trash": {"general_waste"}
}

def verify_predictions(
    predicted_object: str,
    object_confidence: float,
    predicted_category: str,
    category_confidence: float,
    threshold: float = CONFIDENCE_THRESHOLD
) -> Dict[str, Any]:
    """
    Verifies confidence scores against threshold and evaluates logical compatibility
    between object prediction and category prediction per Section 23 & 24 of project README.
    """
    # 1. Confidence Check
    if object_confidence < threshold or category_confidence < threshold:
        return {
            "identifiable": False,
            "object": None,
            "object_confidence": object_confidence,
            "category": None,
            "category_confidence": category_confidence,
            "compatible": False,
            "mapped_category": None,
            "message": "The item could not be identified confidently. Please upload a clearer image or ensure that the image contains a trash item."
        }
        
    # 2. Logical Compatibility Check
    valid_categories = OBJECT_CATEGORY_COMPATIBILITY.get(predicted_object, set())
    is_compatible = predicted_category in valid_categories
    
    # Deterministic mapping fallback for recommendation engine
    mapped_category = predicted_category if is_compatible else (list(valid_categories)[0] if valid_categories else predicted_category)
    
    return {
        "identifiable": True,
        "object": predicted_object,
        "object_confidence": round(object_confidence, 4),
        "category": predicted_category,
        "category_confidence": round(category_confidence, 4),
        "compatible": is_compatible,
        "mapped_category": mapped_category,
        "message": "Item successfully identified and verified." if is_compatible else "Model predictions show disagreement between predicted object and predicted waste category."
    }
