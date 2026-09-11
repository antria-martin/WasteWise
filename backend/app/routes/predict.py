import time
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional

from app.preprocessing.image import preprocess_image
from app.mappings.compatibility import verify_predictions
from app.inference.object_classifier import ObjectClassifier
from app.inference.category_classifier import CategoryClassifier

router = APIRouter()

# Global instances initialized during FastAPI lifespan/startup
object_classifier: Optional[ObjectClassifier] = None
category_classifier: Optional[CategoryClassifier] = None

def init_services():
    global object_classifier, category_classifier
    if object_classifier is None:
        object_classifier = ObjectClassifier()
    if category_classifier is None:
        category_classifier = CategoryClassifier()

@router.post("/predict")
async def predict_waste_item(
    image: UploadFile = File(...),
    enable_center_crop: bool = Form(True),
    enable_white_bg: bool = Form(True),
    enable_lighting_norm: bool = Form(True)
):
    """
    Computer Vision & Compatibility Verification Endpoint.
    Accepts multipart/form-data image upload.
    Runs low-latency image preprocessing, dual MobileNetV3-Small TFLite inference,
    and confidence & logical compatibility verification.
    """
    init_services()

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    try:
        contents = await image.read()
        
        # Measure latency components
        t0 = time.time()
        
        # 1. Low-latency Image Preprocessing
        input_tensor, b64_preview = preprocess_image(
            contents,
            enable_center_crop=enable_center_crop,
            enable_white_bg=enable_white_bg,
            enable_lighting_norm=enable_lighting_norm
        )
        
        # 2. Parallel Dual Model TFLite Inference
        obj_label, obj_conf, obj_top_k = object_classifier.predict(input_tensor, top_k=3)
        cat_label, cat_conf, cat_top_k = category_classifier.predict(input_tensor, top_k=3)
        t_cv = time.time()
        
        # 3. Confidence & Logical Compatibility Verification
        verification = verify_predictions(
            predicted_object=obj_label,
            object_confidence=obj_conf,
            predicted_category=cat_label,
            category_confidence=cat_conf
        )
        
        cv_latency_ms = round((t_cv - t0) * 1000, 2)
        
        # Construct prediction response
        response = {
            "identifiable": verification["identifiable"],
            "object": verification["object"],
            "object_confidence": verification["object_confidence"],
            "category": verification["category"],
            "category_confidence": verification["category_confidence"],
            "mapped_category": verification["mapped_category"],
            "compatible": verification["compatible"],
            "message": verification["message"],
            "top_object_predictions": obj_top_k,
            "top_category_predictions": cat_top_k,
            "latency": {
                "cv_latency_ms": cv_latency_ms
            },
            "preprocessed_preview": b64_preview
        }
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

