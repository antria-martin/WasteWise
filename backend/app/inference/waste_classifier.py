"""
Single-model PyTorch TorchScript inference runner for the WasteWise classifier.

The model (mobilenetv3_trashbox.torchscript.pt) outputs a flat softmax over all
object classes. The predicted class index is decoded to a human-readable object label
via `class_names`, then mapped to a waste category via `object_to_category`.

Expected inference_bundle.json structure:
{
  "img_size": 224,
  "mean": [0.485, 0.456, 0.406],
  "std":  [0.229, 0.224, 0.225],
  "class_names": ["beverage_cans", "cardboard", ...],
  "object_to_category": {
    "beverage_cans": "metal",
    "cardboard": "cardboard",
    ...
  }
}
"""

import json
import torch
import torch.nn.functional as F
from typing import List, Dict, Any

from app.config import MODEL_PATH, INFERENCE_BUNDLE_PATH


class WasteClassifier:
    """
    Wraps the TorchScript MobileNetV3 model.
    Decodes flat softmax output index → object label → category using the
    inference bundle's class_names list and object_to_category mapping.
    """

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model: torch.jit.ScriptModule | None = None
        self.class_names: List[str] = []
        self.object_to_category: Dict[str, str] = {}
        self.is_mock = False

        self._load_bundle()
        self._load_model()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_bundle(self):
        """Load class_names and object_to_category from inference_bundle.json."""
        if not INFERENCE_BUNDLE_PATH.exists():
            print(
                f"Notice: {INFERENCE_BUNDLE_PATH.name} not found. "
                "WasteClassifier will run in mock mode."
            )
            return

        with open(INFERENCE_BUNDLE_PATH, "r") as f:
            bundle = json.load(f)

        self.class_names = bundle.get("class_names", [])
        self.object_to_category = bundle.get("object_to_category", {})
        print(
            f"Loaded inference bundle: {len(self.class_names)} classes, "
            f"{len(self.object_to_category)} category mappings from {INFERENCE_BUNDLE_PATH.name}"
        )

    def _load_model(self):
        """Load the TorchScript .pt model with torch.jit.load()."""
        if not MODEL_PATH.exists():
            self.is_mock = True
            print(
                f"Notice: Model file '{MODEL_PATH.name}' not found. "
                "WasteClassifier running in mock mode."
            )
            return

        try:
            self.model = torch.jit.load(MODEL_PATH, map_location=self.device)
            self.model.eval()
            print(f"Loaded TorchScript model: {MODEL_PATH.name} on {self.device}")
        except Exception as exc:
            self.is_mock = True
            print(
                f"Warning: Failed to load model '{MODEL_PATH.name}': {exc}. "
                "Falling back to mock predictor."
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def predict(self, tensor: torch.Tensor, top_k: int = 3) -> Dict[str, Any]:
        """
        Run inference on a preprocessed tensor and return structured results.

        Args:
            tensor:  Float32 tensor of shape (1, C, H, W) from preprocess_image().
            top_k:   Number of top predictions to include.

        Returns:
            {
                "object":            str,   # top predicted object label
                "category":          str,   # mapped waste category
                "confidence":        float, # softmax probability of top class
                "top_k_predictions": [
                    {"object": str, "category": str, "confidence": float},
                    ...
                ]
            }
        """
        if not self.is_mock and self.model is not None:
            return self._real_predict(tensor, top_k)
        return self._mock_predict(tensor, top_k)

    # ------------------------------------------------------------------
    # Internal inference
    # ------------------------------------------------------------------

    def _real_predict(self, tensor: torch.Tensor, top_k: int) -> Dict[str, Any]:
        tensor = tensor.to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)                     # (1, num_classes)
            probabilities = F.softmax(logits, dim=1)[0]    # (num_classes,)

        k = min(top_k, len(probabilities))
        top_probs, top_indices = torch.topk(probabilities, k)

        top_k_predictions: List[Dict[str, Any]] = []
        for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
            obj_label = self._decode_object(idx)
            cat_label = self.object_to_category.get(obj_label, "general_waste")
            top_k_predictions.append({
                "object":     obj_label,
                "category":   cat_label,
                "confidence": round(prob, 4),
            })

        best = top_k_predictions[0]
        return {
            "object":            best["object"],
            "category":          best["category"],
            "confidence":        best["confidence"],
            "top_k_predictions": top_k_predictions,
        }

    def _decode_object(self, idx: int) -> str:
        """Map a class index to its object label string."""
        if idx < len(self.class_names):
            return self.class_names[idx]
        return f"class_{idx}"

    # ------------------------------------------------------------------
    # Mock fallback (for development without model file)
    # ------------------------------------------------------------------

    def _mock_predict(self, tensor: torch.Tensor, top_k: int) -> Dict[str, Any]:
        """Deterministic mock prediction based on tensor mean when model is absent."""
        mean_val = float(tensor.mean().item())
        num_classes = max(1, len(self.class_names))
        hash_idx = int(abs(mean_val) * 1000 * 17) % num_classes

        def make_entry(idx: int, confidence: float) -> Dict[str, Any]:
            obj = self._decode_object(idx)
            cat = self.object_to_category.get(obj, "general_waste")
            return {"object": obj, "category": cat, "confidence": confidence}

        primary = make_entry(hash_idx, 0.93)
        top_k_predictions = [primary]
        for i in range(1, min(top_k, num_classes)):
            other_idx = (hash_idx + i) % num_classes
            top_k_predictions.append(make_entry(other_idx, round(max(0.01, 0.05 / (i + 1)), 2)))

        return {
            "object":            primary["object"],
            "category":          primary["category"],
            "confidence":        primary["confidence"],
            "top_k_predictions": top_k_predictions,
        }
