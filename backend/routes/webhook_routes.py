"""Webhook routes - endpoint management and incoming webhook receiver."""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from backend.services.webhook_service import (
    create_endpoint,
    process_incoming_request,
    get_events,
    get_endpoint,
    list_endpoints,
    clear_events,
    delete_endpoint,
)

router = APIRouter(tags=["Webhook"])


@router.post("/webhooks/create")
async def create_webhook_endpoint(request: Request):
    """Create a new webhook endpoint."""
    base_url = str(request.base_url).rstrip("/")
    endpoint = create_endpoint(base_url)
    return endpoint.model_dump()


@router.get("/webhooks/list")
async def list_webhook_endpoints():
    """List all active webhook endpoints."""
    return [ep.model_dump() for ep in list_endpoints()]


@router.get("/webhooks/{endpoint_id}/events")
async def get_webhook_events(endpoint_id: str):
    """Get all captured events for a webhook endpoint."""
    events = get_events(endpoint_id)
    return [e.model_dump() for e in events]


@router.delete("/webhooks/{endpoint_id}/events")
async def clear_webhook_events(endpoint_id: str):
    """Clear all events for a webhook endpoint."""
    clear_events(endpoint_id)
    return {"success": True}


@router.delete("/webhooks/{endpoint_id}")
async def delete_webhook(endpoint_id: str):
    """Delete a webhook endpoint."""
    delete_endpoint(endpoint_id)
    return {"success": True}


@router.api_route(
    "/hook/{endpoint_id}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
)
async def receive_webhook(endpoint_id: str, request: Request):
    """
    Universal webhook receiver.
    Accepts ANY method and ANY content type.
    Always returns {"success": true}.
    """
    # Read raw body bytes
    raw_bytes = await request.body()
    raw_body = raw_bytes.decode("utf-8", errors="replace")

    # Extract headers as dict
    headers = dict(request.headers)

    # Extract query params
    query_params = dict(request.query_params)

    # Client IP
    client_ip = request.client.host if request.client else "unknown"

    event = process_incoming_request(
        endpoint_id=endpoint_id,
        method=request.method,
        headers=headers,
        query_params=query_params,
        raw_body=raw_body,
        client_ip=client_ip,
        path=str(request.url.path),
    )

    if event is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Webhook endpoint not found"},
        )

    return {"success": True}
