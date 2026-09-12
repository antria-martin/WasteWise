import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from app.recommendation.llm_service import LLMRecommendationEngine

router = APIRouter()

# Global LLM engine instance initialized during FastAPI lifespan/startup
llm_engine: Optional[LLMRecommendationEngine] = None

def init_recommend_services():
    global llm_engine
    if llm_engine is None:
        llm_engine = LLMRecommendationEngine()

class RecommendRequest(BaseModel):
    predicted_object: str = Field(
        ..., 
        description="Verified item label from prediction endpoint (e.g. 'plastic_bottles')"
    )
    predicted_category: str = Field(
        ..., 
        description="Verified waste category from prediction endpoint (e.g. 'plastic')"
    )
    confidence: float = Field(
        default=1.0, 
        ge=0.0, 
        le=1.0, 
        description="Prediction confidence score from the model"
    )

@router.post("/recommend")
async def get_sustainability_recommendation(payload: RecommendRequest):
    """
    LLM & Knowledge Base Sustainability Recommendation Endpoint.
    Accepts JSON body with verified object & category predictions.
    Queries the Waste Rule Engine (knowledge base) and synthesizes
    encouraging natural language sustainability guidance via Gemini LLM.
    """
    init_recommend_services()

    try:
        t0 = time.time()
        
        recommendation = llm_engine.generate_recommendation(
            predicted_object=payload.predicted_object,
            predicted_category=payload.predicted_category,
            confidence=payload.confidence,
        )
        
        t_end = time.time()
        recommendation_latency_ms = round((t_end - t0) * 1000, 2)
        
        return {
            "status": "success",
            "recommendation": recommendation,
            "latency": {
                "recommendation_latency_ms": recommendation_latency_ms
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")
