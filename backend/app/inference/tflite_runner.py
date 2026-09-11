import os
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

# Try loading tflite_runtime or tensorflow.lite
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow.lite as tflite
    except ImportError:
        tflite = None


class TFLiteClassifier:
    """
    Generic TFLite Model Classifier Wrapper.
    Handles interpreter startup, tensor allocation, and inference execution.
    Provides a mock fallback when pre-trained .tflite files are missing.
    """
    def __init__(self, model_path: Path, labels_path: Path, model_name: str = "TFLiteModel"):
        self.model_path = model_path
        self.labels_path = labels_path
        self.model_name = model_name
        self.labels: List[str] = []
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.is_mock = False

        self._load_labels()
        self._load_model()

    def _load_labels(self):
        if self.labels_path.exists():
            with open(self.labels_path, "r", encoding="utf-8") as f:
                self.labels = [line.strip() for line in f if line.strip()]
        else:
            self.labels = ["unknown"]

    def _load_model(self):
        if self.model_path.exists() and tflite is not None:
            try:
                self.interpreter = tflite.Interpreter(model_path=str(self.model_path))
                self.interpreter.allocate_tensors()
                self.input_details = self.interpreter.get_input_details()
                self.output_details = self.interpreter.get_output_details()
                print(f"Loaded TFLite model successfully: {self.model_path.name}")
                return
            except Exception as e:
                print(f"Warning: Failed to load TFLite model '{self.model_path.name}': {e}. Falling back to mock predictor.")

        # Fallback to mock if model file is not present yet
        self.is_mock = True
        print(f"Notice: Pre-trained file '{self.model_path.name}' not found yet. TFLiteClassifier initialized in mock mode.")

    def predict(self, input_tensor: np.ndarray, top_k: int = 3) -> Tuple[str, float, List[Tuple[str, float]]]:
        """
        Runs inference on preprocessed input_tensor shape (1, 224, 224, 3).
        Returns:
          - top_label: predicted class label (str)
          - top_confidence: prediction confidence score (float)
          - top_predictions: list of (label, confidence) tuples
        """
        if not self.is_mock and self.interpreter is not None:
            # Check quantization/input type
            input_type = self.input_details[0]['dtype']
            if input_type == np.uint8:
                tensor_input = (input_tensor * 255.0).astype(np.uint8)
            else:
                tensor_input = input_tensor.astype(np.float32)

            self.interpreter.set_tensor(self.input_details[0]['index'], tensor_input)
            self.interpreter.invoke()
            
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            
            # Apply Softmax if outputs are logits
            if np.max(output_data) > 1.0 or np.min(output_data) < 0.0:
                exp_scores = np.exp(output_data - np.max(output_data))
                probabilities = exp_scores / np.sum(exp_scores)
            else:
                probabilities = output_data
                
            sorted_indices = np.argsort(probabilities)[::-1]
            
            top_predictions = [
                (self.labels[idx] if idx < len(self.labels) else f"class_{idx}", float(probabilities[idx]))
                for idx in sorted_indices[:top_k]
            ]
            
            top_label, top_confidence = top_predictions[0]
            return top_label, top_confidence, top_predictions

        # Mock inference implementation for development/testing prior to placing .tflite files
        return self._mock_predict(input_tensor, top_k)

    def _mock_predict(self, input_tensor: np.ndarray, top_k: int) -> Tuple[str, float, List[Tuple[str, float]]]:
        """Generates deterministic mock prediction based on image color profile when model file is absent."""
        avg_r = float(np.mean(input_tensor[0, :, :, 0]))
        avg_g = float(np.mean(input_tensor[0, :, :, 1]))
        avg_b = float(np.mean(input_tensor[0, :, :, 2]))

        num_classes = len(self.labels)
        # Hash color values to get consistent mock prediction per image
        hash_idx = int((avg_r * 100 + avg_g * 50 + avg_b * 25) * 17) % max(1, num_classes)
        
        primary_label = self.labels[hash_idx] if hash_idx < len(self.labels) else self.labels[0]
        confidence = 0.94 if "object" in self.model_name.lower() else 0.91

        predictions = [(primary_label, confidence)]
        for i in range(1, min(top_k, num_classes)):
            other_idx = (hash_idx + i) % num_classes
            predictions.append((self.labels[other_idx], round(max(0.01, 0.05 / (i + 1)), 2)))

        return primary_label, confidence, predictions
