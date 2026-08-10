from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and Shutdown Events
    """

    print("=" * 60)
    print("🚀 AI Document Intelligence Agent Started")
    print("=" * 60)

    yield

    print("=" * 60)
    print("🛑 AI Document Intelligence Agent Stopped")
    print("=" * 60)


app = FastAPI(
    title="AI Document Intelligence Agent",
    description="""
AI-powered Document Intelligence System using:

✅ FastAPI

✅ LangGraph

✅ RapidOCR

✅ EasyOCR

✅ Google Gemini

✅ Multi-Agent Architecture
""",
    version="2.0.0",
    lifespan=lifespan,
)

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include API Routes
# -----------------------------
app.include_router(router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/", tags=["Home"])
async def home():
    return {
        "success": True,
        "application": "AI Document Intelligence Agent",
        "version": "2.0.0",
        "status": "Running",
        "documentation": "/docs",
    }

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health", tags=["Health"])
async def health():
    return {
        "success": True,
        "status": "Healthy",
        "service": "AI Document Intelligence Agent",
    }