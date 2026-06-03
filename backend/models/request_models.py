"""Pydantic models for API tester request/response."""

from typing import Optional
from pydantic import BaseModel


class OutgoingRequest(BaseModel):
    """Model for an API test request to be sent."""
    method: str
    url: str
    headers: dict[str, str] = {}
    params: dict[str, str] = {}
    body: Optional[str] = None
    auth_type: str = "None"
    auth_value: Optional[str] = None
    timeout: float = 30.0


class OutgoingResponse(BaseModel):
    """Model for the result of an API test request."""
    status_code: int
    headers: dict[str, str]
    body: str
    elapsed_ms: float
    error: Optional[str] = None
