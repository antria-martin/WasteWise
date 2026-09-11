import io
import sys
import numpy as np
from PIL import Image
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.preprocessing.image import preprocess_image
from app.mappings.compatibility import verify_predictions, OBJECT_CATEGORY_COMPATIBILITY
from app.recommendation.rule_engine import WasteRuleEngine

client = TestClient(app)

def create_sample_image_bytes():
    """Generates 300x300 RGB test image bytes."""
    img = Image.new("RGB", (300, 300), color=(100, 150, 200))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "confidence_threshold" in data

def test_preprocessing_pipeline():
    img_bytes = create_sample_image_bytes()
    input_tensor, b64_preview = preprocess_image(
        img_bytes,
        enable_center_crop=True,
        enable_white_bg=True,
        enable_lighting_norm=True
    )
    assert input_tensor.shape == (1, 224, 224, 3)
    assert input_tensor.dtype == np.float32
    assert b64_preview.startswith("data:image/jpeg;base64,")

def test_compatibility_verification_pass():
    res = verify_predictions("plastic_bottle", 0.94, "plastic", 0.91, threshold=0.70)
    assert res["identifiable"] is True
    assert res["compatible"] is True
    assert res["mapped_category"] == "plastic"

def test_compatibility_verification_low_confidence():
    # Low confidence must yield identifiable: False per project spec (no general_waste fallback)
    res = verify_predictions("plastic_bottle", 0.40, "plastic", 0.55, threshold=0.70)
    assert res["identifiable"] is False
    assert res["object"] is None
    assert res["category"] is None

def test_compatibility_verification_mismatch():
    res = verify_predictions("plastic_bottle", 0.85, "glass", 0.88, threshold=0.70)
    assert res["identifiable"] is True
    assert res["compatible"] is False

def test_rule_engine():
    engine = WasteRuleEngine()
    info = engine.get_category_info("plastic")
    assert info["recyclable"] is True
    assert "disposal_instructions" in info

def test_predict_endpoint():
    img_bytes = create_sample_image_bytes()
    response = client.post(
        "/api/predict",
        files={"image": ("test.jpg", img_bytes, "image/jpeg")},
        data={
            "enable_center_crop": "true",
            "enable_white_bg": "true",
            "enable_lighting_norm": "true"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "identifiable" in data
    assert "object_confidence" in data
    assert "category_confidence" in data
    assert "latency" in data
    assert "preprocessed_preview" in data

def test_recommend_endpoint():
    payload = {
        "predicted_object": "plastic_bottle",
        "predicted_category": "plastic",
        "confidence": 0.94,
        "is_compatible": True
    }
    response = client.post("/api/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "recommendation" in data
    rec = data["recommendation"]
    assert rec["object"] == "plastic_bottle"
    assert rec["category"] == "plastic"
    assert rec["recyclable"] is True
    assert "disposal_instructions" in rec

def test_decoupled_flow():
    # Step 1: Predict
    img_bytes = create_sample_image_bytes()
    pred_res = client.post(
        "/api/predict",
        files={"image": ("test.jpg", img_bytes, "image/jpeg")},
        data={"enable_center_crop": "true"}
    )
    assert pred_res.status_code == 200
    pred_data = pred_res.json()
    
    if pred_data["identifiable"] and pred_data["compatible"]:
        # Step 2: Recommend
        rec_res = client.post("/api/recommend", json={
            "predicted_object": pred_data["object"],
            "predicted_category": pred_data["mapped_category"],
            "confidence": pred_data["object_confidence"],
            "is_compatible": True
        })
        assert rec_res.status_code == 200
        rec_data = rec_res.json()
        assert rec_data["status"] == "success"
        assert "recommendation" in rec_data

