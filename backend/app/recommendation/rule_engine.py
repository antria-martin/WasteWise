import json
from pathlib import Path
from typing import Dict, Any

KNOWLEDGE_BASE_PATH = Path(__file__).resolve().parent / "knowledge_base.json"

class WasteRuleEngine:
    def __init__(self):
        self.kb: Dict[str, Any] = {}
        self._load_kb()

    def _load_kb(self):
        if KNOWLEDGE_BASE_PATH.exists():
            with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
                self.kb = json.load(f)

    def get_category_info(self, category: str) -> Dict[str, Any]:
        """Returns ground truth knowledge base entry for a waste category."""
        normalized_cat = category.lower().strip()
        if normalized_cat in self.kb:
            return self.kb[normalized_cat]
        return self.kb.get("general_waste", {
            "recyclable": False,
            "recommended_action": "Dispose in General Waste Bin",
            "disposal_instructions": ["Dispose in general trash."],
            "reuse_ideas": ["No specific reuse guidance."],
            "upcycling_ideas": ["No specific upcycling guidance."],
            "safety_warnings": ["Handle waste responsibly."]
        })
