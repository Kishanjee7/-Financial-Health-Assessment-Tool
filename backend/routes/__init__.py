"""Routes package initialization."""
from routes.upload import router as upload_router
from routes.analysis import router as analysis_router
from routes.reports import router as reports_router
from routes.integrations import router as integrations_router

__all__ = ["upload_router", "analysis_router", "reports_router", "integrations_router"]
