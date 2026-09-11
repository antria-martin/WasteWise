from app.config import OBJECT_MODEL_PATH, OBJECT_LABELS_PATH
from app.inference.tflite_runner import TFLiteClassifier

class ObjectClassifier(TFLiteClassifier):
    def __init__(self):
        super().__init__(
            model_path=OBJECT_MODEL_PATH,
            labels_path=OBJECT_LABELS_PATH,
            model_name="ObjectIdentificationModel"
        )
