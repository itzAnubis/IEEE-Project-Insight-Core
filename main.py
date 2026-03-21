"""
Session Management & Metrics API — Main Application Entry Point.

This is the FastAPI application factory. It:
  1. Configures structured logging
  2. Registers the API router from src.api.routes
  3. On startup: initializes the database and seeds sample data
  4. Provides a root health-check endpoint

Integration note:
  If integrating with an existing main.py managed by a Squad Lead, 
  you can import `api_router` from src.api.routes and include it:
      from src.api.routes import router as api_router
      app.include_router(api_router)
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.routes import router as api_router
from src.api.db import init_db, seed_data

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)-15s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("api.main")


# ---------------------------------------------------------------------------
# Application lifespan (startup / shutdown)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB + seed data. Shutdown: cleanup."""
    logger.info("=" * 60)
    logger.info("APPLICATION STARTUP")
    logger.info("=" * 60)
    init_db()
    seed_data()
    logger.info("Startup complete — API is ready")
    yield
    logger.info("APPLICATION SHUTDOWN")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Session Management & Metrics API",
    description=(
        "A production-ready API for managing educational sessions with "
        "real-time background data generation, SQLite-backed metrics, "
        "and comprehensive session lifecycle management."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Register API routes
app.include_router(api_router)


# ---------------------------------------------------------------------------
# Global exception handlers
# ---------------------------------------------------------------------------
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """Return consistent JSON for HTTP errors."""
    detail = exc.detail
    if isinstance(detail, dict):
        return JSONResponse(status_code=exc.status_code, content=detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": str(detail),
            "data": None,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Return consistent JSON for validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Request validation failed",
            "data": exc.errors(),
        },
    )


# ---------------------------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    """Health check / welcome endpoint."""
    return {
        "status": "success",
        "message": "Session Management & Metrics API is running",
        "data": {
            "version": "1.0.0",
            "docs": "/docs",
            "endpoints_prefix": "/api",
        },
    }
