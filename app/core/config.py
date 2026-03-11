import os

# Project root directory (two levels up from app/core/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Database
DB_PATH = os.path.join(BASE_DIR, "database", "project.db")

# Application
APP_TITLE = "Insight Core API"
APP_VERSION = "1.0.0"
API_PREFIX = "/api"

# Logging
LOG_LEVEL = "INFO"
