"""Shared constants used across the application."""

# Supported HTTP methods
HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

# Authentication types
AUTH_TYPES = ["None", "Bearer Token", "Basic Auth", "API Key"]

# Content types supported by webhook receiver
SUPPORTED_CONTENT_TYPES = [
    "application/json",
    "multipart/form-data",
    "application/x-www-form-urlencoded",
    "text/plain",
    "application/xml",
]

# Backend configuration
BACKEND_HOST = "localhost"
BACKEND_PORT = 8000
BACKEND_BASE_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# Request defaults
DEFAULT_TIMEOUT = 30.0
MAX_HISTORY_SIZE = 50
MAX_WEBHOOK_EVENTS = 100
