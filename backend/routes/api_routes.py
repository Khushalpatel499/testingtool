"""API routes for the API Tester module."""

from fastapi import APIRouter, Header
from typing import Optional

from backend.models.request_models import OutgoingRequest
from backend.services.request_service import execute_request
from backend.storage.history_store import history_store

router = APIRouter(prefix="/api", tags=["API Tester"])


@router.post("/send")
async def send_request(request: OutgoingRequest, x_session_id: Optional[str] = Header(default="default")):
    """Execute an outgoing HTTP request and return the response."""
    response = await execute_request(request, session_id=x_session_id)
    return response.model_dump()


@router.get("/history")
async def get_history(x_session_id: Optional[str] = Header(default="default")):
    """Get request history for the current session."""
    return history_store.get_all(session_id=x_session_id)


@router.delete("/history")
async def clear_history(x_session_id: Optional[str] = Header(default="default")):
    """Clear request history for the current session."""
    history_store.clear(session_id=x_session_id)
    return {"success": True}
