"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.api_routes import router as api_router
from backend.routes.webhook_routes import router as webhook_router

app = FastAPI(
    title="DevTool API",
    description="API Tester + Webhook Inspector Backend",
    version="1.0.0",
)

# Allow Streamlit frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(api_router)
app.include_router(webhook_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
