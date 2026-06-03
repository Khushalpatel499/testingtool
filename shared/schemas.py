"""Shared Pydantic schemas defining API contracts between frontend and backend."""

from typing import Any, Optional
from pydantic import BaseModel


class ApiRequestSchema(BaseModel):
    """Schema for outgoing API test requests."""
    method: str
    url: str
    headers: dict[str, str] = {}
    params: dict[str, str] = {}
    body: Optional[str] = None
    auth_type: str = "None"
    auth_value: Optional[str] = None
    timeout: float = 30.0


class ApiResponseSchema(BaseModel):
    """Schema for API test response data."""
    status_code: int
    headers: dict[str, str]
    body: str
    elapsed_ms: float
    error: Optional[str] = None


class WebhookEventSchema(BaseModel):
    """Schema for a captured webhook event."""
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


class WebhookEndpointSchema(BaseModel):
    """Schema for a webhook endpoint."""
    id: str
    url: str
    created_at: str
    event_count: int = 0
