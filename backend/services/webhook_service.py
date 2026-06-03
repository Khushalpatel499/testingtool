"""Webhook service - manages endpoints and processes incoming webhook events."""

import uuid
from datetime import datetime, timezone

from backend.models.webhook_models import WebhookEvent, WebhookEndpoint
from backend.services.parser_service import parse_body
from backend.storage.webhook_store import webhook_store
from backend.utils.ua_parser import parse_user_agent


def create_endpoint(base_url: str, session_id: str) -> WebhookEndpoint:
    """Create a new webhook endpoint with a random ID."""
    endpoint_id = uuid.uuid4().hex[:12]
    endpoint = WebhookEndpoint(
        id=endpoint_id,
        url=f"{base_url}/hook/{endpoint_id}",
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    webhook_store.create_endpoint(session_id, endpoint)
    return endpoint


def process_incoming_request(
    endpoint_id: str,
    method: str,
    headers: dict[str, str],
    query_params: dict[str, str],
    raw_body: str,
    client_ip: str,
    path: str,
) -> WebhookEvent | None:
    """Process an incoming webhook request and store the event."""
    if not webhook_store.endpoint_exists(endpoint_id):
        return None

    content_type = headers.get("content-type", headers.get("Content-Type"))
    parsed = parse_body(content_type, raw_body)

    # Parse device info from User-Agent header
    user_agent = headers.get("user-agent", headers.get("User-Agent", ""))
    device_info = parse_user_agent(user_agent)

    event = WebhookEvent(
        id=uuid.uuid4().hex[:16],
        endpoint_id=endpoint_id,
        method=method,
        headers=headers,
        query_params=query_params,
        content_type=content_type,
        raw_body=raw_body,
        parsed_body=parsed,
        client_ip=client_ip,
        path=path,
        timestamp=datetime.now(timezone.utc).isoformat(),
        device_info=device_info,
    )
    webhook_store.add_event(event)
    return event


def get_events(endpoint_id: str) -> list[WebhookEvent]:
    return webhook_store.get_events(endpoint_id)


def get_endpoint(endpoint_id: str) -> WebhookEndpoint | None:
    return webhook_store.get_endpoint(endpoint_id)


def list_endpoints(session_id: str) -> list[WebhookEndpoint]:
    """List endpoints belonging to this session only."""
    return webhook_store.list_endpoints(session_id)


def clear_events(endpoint_id: str) -> None:
    webhook_store.clear_events(endpoint_id)


def delete_endpoint(endpoint_id: str) -> None:
    webhook_store.delete_endpoint(endpoint_id)
