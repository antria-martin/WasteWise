from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routes.predict import router as predict_router, init_services
from app.routes.recommend import router as recommend_router, init_recommend_services
from app.routes.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load model interpreters once in memory
    print("Starting WasteWise FastAPI Backend Service...")
    init_services()
    init_recommend_services()
    print("Inference interpreters and recommendation engines initialized.")
    yield
    # Shutdown: clean up
    print("Shutting down WasteWise service...")

app = FastAPI(
    title="WasteWise AI Backend",
    description="AI-Driven Waste Identification System with TFLite Computer Vision and LLM Sustainability Recommendations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for Flutter mobile app and Web client access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(predict_router, prefix="/api", tags=["Prediction"])
app.include_router(recommend_router, prefix="/api", tags=["Recommendation"])

# Serve static web testing interface
STATIC_DIR = Path(__file__).resolve().parent / "static"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
