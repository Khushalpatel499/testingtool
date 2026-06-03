"""Service layer for executing outgoing HTTP requests (API Tester engine)."""

import time
import base64
import httpx

from backend.models.request_models import OutgoingRequest, OutgoingResponse
from backend.storage.history_store import history_store


def _build_auth_headers(auth_type: str, auth_value: str | None) -> dict[str, str]:
    """Build authentication headers based on auth type."""
    if not auth_value:
        return {}

    if auth_type == "Bearer Token":
        return {"Authorization": f"Bearer {auth_value}"}
    elif auth_type == "Basic Auth":
        encoded = base64.b64encode(auth_value.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}
    elif auth_type == "API Key":
        parts = auth_value.split(":", 1)
        if len(parts) == 2:
            return {parts[0]: parts[1]}
    return {}


async def execute_request(request: OutgoingRequest, session_id: str) -> OutgoingResponse:
    """Execute an HTTP request and return the response."""
    headers = {**request.headers, **_build_auth_headers(request.auth_type, request.auth_value)}
    content = request.body.encode() if request.body else None

    try:
        async with httpx.AsyncClient(timeout=request.timeout, follow_redirects=True) as client:
            start = time.perf_counter()
            resp = await client.request(
                method=request.method,
                url=request.url,
                headers=headers,
                params=request.params or None,
                content=content,
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

        response = OutgoingResponse(
            status_code=resp.status_code,
            headers=dict(resp.headers),
            body=resp.text,
            elapsed_ms=round(elapsed_ms, 2),
        )
    except httpx.TimeoutException:
        response = OutgoingResponse(
            status_code=0, headers={}, body="", elapsed_ms=0,
            error="Request timed out",
        )
    except httpx.InvalidURL:
        response = OutgoingResponse(
            status_code=0, headers={}, body="", elapsed_ms=0,
            error="Invalid URL provided",
        )
    except Exception as e:
        response = OutgoingResponse(
            status_code=0, headers={}, body="", elapsed_ms=0,
            error=str(e),
        )

    # Store in session-based history
    history_store.add(session_id, request, response)
    return response
