import os
from typing import Dict, Any, List
from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.recommendation.rule_engine import WasteRuleEngine

# Try importing google-genai or google.generativeai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class LLMRecommendationEngine:
    def __init__(self):
        self.rule_engine = WasteRuleEngine()
        self.client = None
        
        api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        if api_key and GENAI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=api_key)
                print(f"Initialized Gemini LLM Client ({GEMINI_MODEL})")
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")

    def generate_recommendation(
        self,
        predicted_object: str,
        predicted_category: str,
        confidence: float,
    ) -> Dict[str, Any]:
        """
        Combines verified knowledge base facts with LLM synthesis to produce
        actionable, natural language sustainability guidance.
        """
        # Fetch ground truth knowledge
        kb_info = self.rule_engine.get_category_info(predicted_category)

        # Base fallback recommendation payload
        fallback_response = {
            "object": predicted_object,
            "category": predicted_category,
            "recyclable": kb_info.get("recyclable", False),
            "recommended_action": kb_info.get("recommended_action", "Dispose properly"),
            "disposal_instructions": kb_info.get("disposal_instructions", []),
            "reuse_ideas": kb_info.get("reuse_ideas", []),
            "upcycling_ideas": kb_info.get("upcycling_ideas", []),
            "safety_warnings": kb_info.get("safety_warnings", []),
            "summary": f"Identified {predicted_object.replace('_', ' ')} (Category: {predicted_category.upper()}). {kb_info.get('recommended_action')}.",
            "llm_enhanced": False
        }

        if self.client is not None:
            try:
                prompt = f"""
You are an expert Sustainability and Waste Management Assistant.
Generate concise, structured, user-friendly sustainability recommendations for the following item:

Item Name: {predicted_object.replace('_', ' ')}
Category: {predicted_category}
Verified Category Rules:
- Recommended Action: {kb_info.get('recommended_action')}
- Disposal Steps: {', '.join(kb_info.get('disposal_instructions', []))}
- Standard Reuse: {', '.join(kb_info.get('reuse_ideas', []))}
- Upcycling Ideas: {', '.join(kb_info.get('upcycling_ideas', []))}
- Safety Guidelines: {', '.join(kb_info.get('safety_warnings', []))}

Provide your response formatted clearly under these sections:
1. Executive Summary (1-2 sentences)
2. Step-by-Step Recycling/Disposal Preparation
3. Creative Practical Reuse Project
4. Inspiring DIY Upcycling Project
5. Crucial Safety Advice
Do NOT contradict the verified rules. Keep tone encouraging and actionable.
"""
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )
                if response and response.text:
                    fallback_response["summary"] = response.text.strip()
                    fallback_response["llm_enhanced"] = True
            except Exception as e:
                print(f"Notice: LLM API call failed ({e}). Returning verified knowledge base guidance.")

        return fallback_response
