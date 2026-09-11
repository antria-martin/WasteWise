from app.config import CATEGORY_MODEL_PATH, CATEGORY_LABELS_PATH
from app.inference.tflite_runner import TFLiteClassifier

class CategoryClassifier(TFLiteClassifier):
    def __init__(self):
        super().__init__(
            model_path=CATEGORY_MODEL_PATH,
            labels_path=CATEGORY_LABELS_PATH,
            model_name="WasteCategoryModel"
        )
