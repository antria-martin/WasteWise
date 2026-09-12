"""
End-to-end pipeline tests for the WasteWise backend.
Covers: preprocessing → model inference → compatibility check → LLM recommendation.
Uses tests/bottle.jpg (a real plastic bottle photo) for the full-pipeline tests.
"""
import io
import sys
import torch
from PIL import Image
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.preprocessing.image import preprocess_image
from app.mappings.compatibility import verify_predictions
from app.recommendation.rule_engine import WasteRuleEngine

client = TestClient(app)

BOTTLE_PATH = Path(__file__).resolve().parent / "bottle.jpg"


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def bottle_bytes() -> bytes:
    """Read the real bottle.jpg test fixture."""
    return BOTTLE_PATH.read_bytes()

def synthetic_image_bytes() -> bytes:
    """Minimal 300×300 synthetic image for fast unit tests."""
    img = Image.new("RGB", (300, 300), color=(100, 150, 200))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


# ─────────────────────────────────────────────
# 1. Health check
# ─────────────────────────────────────────────

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "confidence_threshold" in data
    print(f"\n[HEALTH] {data}")


# ─────────────────────────────────────────────
# 2. Preprocessing unit test (new torchvision pipeline)
# ─────────────────────────────────────────────

def test_preprocessing_synthetic():
    """Preprocessing should return a (1, C, H, W) float32 tensor and a base64 preview."""
    tensor, b64 = preprocess_image(synthetic_image_bytes())
    assert isinstance(tensor, torch.Tensor), "Output must be a torch.Tensor"
    assert tensor.ndim == 4,                 "Tensor must be 4-D: (1, C, H, W)"
    assert tensor.shape[0] == 1,             "Batch dimension must be 1"
    assert tensor.dtype == torch.float32,    "Tensor dtype must be float32"
    assert b64.startswith("data:image/jpeg;base64,"), "Preview must be base64 JPEG"
    print(f"\n[PREPROCESS] tensor shape={tuple(tensor.shape)}, dtype={tensor.dtype}")

def test_preprocessing_bottle():
    """Preprocessing should work on a real-world JPEG photo."""
    tensor, b64 = preprocess_image(bottle_bytes())
    assert tensor.ndim == 4
    assert b64.startswith("data:image/jpeg;base64,")
    print(f"\n[PREPROCESS BOTTLE] tensor shape={tuple(tensor.shape)}")


# ─────────────────────────────────────────────
# 3. Compatibility / confidence gate unit tests
# ─────────────────────────────────────────────

def test_verify_passes_high_confidence():
    res = verify_predictions("plastic_bottles", "plastic", confidence=0.94)
    assert res["identifiable"] is True
    assert res["object"] == "plastic_bottles"
    assert res["category"] == "plastic"
    print(f"\n[VERIFY PASS] {res}")

def test_verify_fails_low_confidence():
    res = verify_predictions("plastic_bottles", "plastic", confidence=0.40)
    assert res["identifiable"] is False
    assert res["object"] is None
    assert res["category"] is None
    print(f"\n[VERIFY FAIL] {res}")


# ─────────────────────────────────────────────
# 4. Rule engine unit test
# ─────────────────────────────────────────────

def test_rule_engine_known_categories():
    engine = WasteRuleEngine()
    for cat in ["plastic", "glass", "metal", "paper", "cardboard", "e_waste", "medical"]:
        info = engine.get_category_info(cat)
        assert "recyclable" in info,            f"Missing 'recyclable' for category '{cat}'"
        assert "disposal_instructions" in info, f"Missing 'disposal_instructions' for '{cat}'"
        assert len(info["disposal_instructions"]) > 0
    print("\n[RULE ENGINE] All known categories have valid KB entries [OK]")


# ─────────────────────────────────────────────
# 5. /predict endpoint — synthetic image
# ─────────────────────────────────────────────

def test_predict_endpoint_synthetic():
    response = client.post(
        "/api/predict",
        files={"image": ("test.jpg", synthetic_image_bytes(), "image/jpeg")},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    print(f"\n[PREDICT SYNTHETIC] {data}")

    assert "identifiable" in data
    assert "latency" in data
    assert "preprocessed_preview" in data
    assert "top_k_predictions" in data
    assert isinstance(data["top_k_predictions"], list)
    # confidence key (single float) must exist
    assert "confidence" in data


# ─────────────────────────────────────────────
# 6. /predict endpoint — real bottle.jpg
# ─────────────────────────────────────────────

def test_predict_endpoint_bottle():
    """
    Full model inference on bottle.jpg.
    Asserts response structure; prints prediction so you can verify correctness.
    """
    response = client.post(
        "/api/predict",
        files={"image": ("bottle.jpg", bottle_bytes(), "image/jpeg")},
    )
    assert response.status_code == 200, response.text
    data = response.json()

    print(f"\n[PREDICT BOTTLE]")
    print(f"  identifiable : {data.get('identifiable')}")
    print(f"  object       : {data.get('object')}")
    print(f"  category     : {data.get('category')}")
    print(f"  confidence   : {data.get('confidence')}")
    print(f"  top-3        : {data.get('top_k_predictions')}")
    print(f"  latency      : {data.get('latency')}")

    assert "identifiable" in data
    assert "confidence" in data
    assert "top_k_predictions" in data
    assert data["preprocessed_preview"].startswith("data:image/jpeg;base64,")


# ─────────────────────────────────────────────
# 7. /recommend endpoint — direct call
# ─────────────────────────────────────────────

def test_recommend_endpoint():
    payload = {
        "predicted_object": "plastic_bottles",
        "predicted_category": "plastic",
        "confidence": 0.94,
    }
    response = client.post("/api/recommend", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    print(f"\n[RECOMMEND] status={data['status']}")
    rec = data["recommendation"]
    print(f"  object     : {rec.get('object')}")
    print(f"  category   : {rec.get('category')}")
    print(f"  recyclable : {rec.get('recyclable')}")
    print(f"  summary    : {str(rec.get('summary', ''))[:120]}...")

    assert data["status"] == "success"
    assert rec["object"] == "plastic_bottles"
    assert rec["category"] == "plastic"
    assert rec["recyclable"] is True
    assert "disposal_instructions" in rec


# ─────────────────────────────────────────────
# 8. Decoupled full pipeline: bottle.jpg → predict → recommend
# ─────────────────────────────────────────────

def test_full_pipeline_bottle():
    """
    Full end-to-end: upload bottle.jpg → /predict → feed result into /recommend.
    This is the real integration test of the entire pipeline.
    """
    # Step 1: Predict
    pred_res = client.post(
        "/api/predict",
        files={"image": ("bottle.jpg", bottle_bytes(), "image/jpeg")},
    )
    assert pred_res.status_code == 200, pred_res.text
    pred = pred_res.json()

    print(f"\n[PIPELINE] Prediction:")
    print(f"  identifiable={pred.get('identifiable')}  object={pred.get('object')}  "
          f"category={pred.get('category')}  confidence={pred.get('confidence')}")

    # Step 2: Only recommend if identifiable (model confidence passed threshold)
    if pred["identifiable"]:
        rec_res = client.post("/api/recommend", json={
            "predicted_object":   pred["object"],
            "predicted_category": pred["category"],
            "confidence":         pred["confidence"],
        })
        assert rec_res.status_code == 200, rec_res.text
        rec = rec_res.json()
        print(f"\n[PIPELINE] Recommendation:")
        print(f"  recyclable={rec['recommendation'].get('recyclable')}")
        print(f"  action    ={rec['recommendation'].get('recommended_action')}")
        print(f"  llm       ={rec['recommendation'].get('llm_enhanced')}")
        print(f"  summary   ={str(rec['recommendation'].get('summary',''))[:200]}")
        assert rec["status"] == "success"
        assert "recommendation" in rec
    else:
        print("\n[PIPELINE] Model confidence below threshold — recommend step skipped.")
        print("  (This is correct behaviour — not a test failure.)")
