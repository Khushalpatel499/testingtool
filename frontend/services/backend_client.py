"""Backend client - service layer for frontend-to-backend communication."""

import os
import uuid
import httpx
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
_TIMEOUT = 60.0


def _get_session_id() -> str:
    """Get or create a unique session ID per browser tab."""
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = uuid.uuid4().hex
    return st.session_state["session_id"]


def _headers() -> dict:
    """Build headers with session ID."""
    return {"X-Session-Id": _get_session_id()}


def send_api_request(payload: dict) -> dict:
    """Send an API test request via the backend."""
    with httpx.Client(timeout=_TIMEOUT) as client:
        resp = client.post(f"{BACKEND_URL}/api/send", json=payload, headers=_headers())
        return resp.json()


def get_history() -> list[dict]:
    """Fetch request history from backend."""
    with httpx.Client(timeout=_TIMEOUT) as client:
        resp = client.get(f"{BACKEND_URL}/api/history", headers=_headers())
        return resp.json()


def clear_history() -> None:
    """Clear request history."""
    with httpx.Client(timeout=_TIMEOUT) as client:
        client.delete(f"{BACKEND_URL}/api/history", headers=_headers())


def create_webhook_endpoint() -> dict:
    """Create a new webhook endpoint."""
    with httpx.Client(timeout=_TIMEOUT) as client:
        resp = client.post(f"{BACKEND_URL}/webhooks/create", headers=_headers())
        return resp.json()


def list_webhook_endpoints() -> list[dict]:
    """List all webhook endpoints for this session."""
    with httpx.Client(timeout=_TIMEOUT) as client:
        resp = client.get(f"{BACKEND_URL}/webhooks/list", headers=_headers())
        return resp.json()


def get_webhook_events(endpoint_id: str) -> list[dict]:
    """Get events for a webhook endpoint."""
    with httpx.Client(timeout=_TIMEOUT) as client:
        resp = client.get(f"{BACKEND_URL}/webhooks/{endpoint_id}/events")
        return resp.json()


def clear_webhook_events(endpoint_id: str) -> None:
    """Clear events for a webhook endpoint."""
    with httpx.Client(timeout=_TIMEOUT) as client:
        client.delete(f"{BACKEND_URL}/webhooks/{endpoint_id}/events")


def delete_webhook_endpoint(endpoint_id: str) -> None:
    """Delete a webhook endpoint."""
    with httpx.Client(timeout=_TIMEOUT) as client:
        client.delete(f"{BACKEND_URL}/webhooks/{endpoint_id}")
