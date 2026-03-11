from fastapi import FastAPI

from app.api.routes import sessions, metrics, reports
from app.core.config import APP_TITLE, APP_VERSION, API_PREFIX
from app.core.logging import logger

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# ───────────────────────────────────────────
# Router Registration
# ───────────────────────────────────────────

app.include_router(sessions.router, prefix=API_PREFIX)
app.include_router(metrics.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)


# ───────────────────────────────────────────
# Lifecycle Events
# ───────────────────────────────────────────

@app.on_event("startup")
def on_startup():
    logger.info(f"{APP_TITLE} v{APP_VERSION} started successfully")


# ───────────────────────────────────────────
# Health Check
# ───────────────────────────────────────────

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Insight Core API running",
    }