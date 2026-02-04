"""
Financial Health Assessment Platform - Main Application
FastAPI entry point with CORS, routes, and startup configuration.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from config import settings
from database import init_db, DatabaseManager
from routes import upload_router, analysis_router, reports_router, integrations_router
from i18n import get_all_translations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Initialize database
    init_db()
    print("Database initialized")
    
    # Create upload directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    print(f"Upload directory: {settings.UPLOAD_DIR}")
    
    yield
    
    # Shutdown
    print("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered financial health assessment platform for SMEs",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(integrations_router, prefix="/api")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "features": [
            "Multi-format document ingestion (CSV, XLSX, PDF)",
            "Comprehensive financial metrics calculation",
            "AI-powered insights and recommendations",
            "Risk assessment and creditworthiness scoring",
            "Industry-specific benchmarking",
            "Financial forecasting",
            "GST compliance checking",
            "Banking API integrations",
            "Multilingual support (English, Hindi)",
            "Investor-ready PDF reports"
        ]
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    db_status = DatabaseManager.health_check()
    return {
        "status": "healthy" if db_status else "degraded",
        "database": "connected" if db_status else "disconnected",
        "version": settings.APP_VERSION
    }


@app.get("/api/translations/{language}")
async def get_translations(language: str = "en"):
    """Get UI translations for a language."""
    if language not in settings.SUPPORTED_LANGUAGES:
        raise HTTPException(400, f"Language not supported. Available: {settings.SUPPORTED_LANGUAGES}")
    
    return {
        "language": language,
        "translations": get_all_translations(language)
    }


@app.get("/api/config")
async def get_config():
    """Get public configuration."""
    return {
        "supported_languages": settings.SUPPORTED_LANGUAGES,
        "default_language": settings.DEFAULT_LANGUAGE,
        "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS,
        "industries": [
            "manufacturing", "retail", "agriculture", "services",
            "logistics", "ecommerce", "healthcare", "construction", "other"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
