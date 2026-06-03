"""Pydantic models for webhook events and endpoints."""

from typing import Any, Optional
from pydantic import BaseModel


class WebhookEvent(BaseModel):
    """Model representing a single captured webhook request."""
    id: str
    endpoint_id: str
    method: str
    headers: dict[str, str]
    query_params: dict[str, str]
    content_type: Optional[str]
    raw_body: str
    parsed_body: Optional[Any] = None
    client_ip: str
    path: str
    timestamp: str
    device_info: Optional[str] = None


class WebhookEndpoint(BaseModel):
    """Model representing a webhook endpoint."""
    id: str
    url: str
    created_at: str
    event_count: int = 0
