import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent


def _path_from_env(name: str, default: Path) -> Path:
    value = os.getenv(name)
    if not value:
        return default

    path = Path(value).expanduser()
    if path.is_absolute():
        return path

    return (BACKEND_DIR / path).resolve()


def _float_from_env(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        return default


MODEL_PATH = _path_from_env(
    "WASTEWISE_MODEL_PATH",
    APP_DIR / "models" / "mobilenetv3_trashbox.torchscript.pt",
)

INFERENCE_BUNDLE_PATH = _path_from_env(
    "WASTEWISE_INFERENCE_BUNDLE_PATH",
    APP_DIR / "models" / "inference_bundle.json",
)

CONFIDENCE_THRESHOLD = _float_from_env("WASTEWISE_CONFIDENCE_THRESHOLD", 0.6)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
