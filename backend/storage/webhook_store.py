"""In-memory storage for webhook endpoints and events — session-based."""

from collections import deque
from backend.models.webhook_models import WebhookEvent, WebhookEndpoint

_MAX_EVENTS = 100


class WebhookStore:
    """Session-based in-memory store for webhook endpoints and their events."""

    def __init__(self) -> None:
        # session_id -> {endpoint_id -> WebhookEndpoint}
        self._endpoints: dict[str, dict[str, WebhookEndpoint]] = {}
        # endpoint_id -> deque of WebhookEvent (shared, since external services hit these)
        self._events: dict[str, deque[WebhookEvent]] = {}
        # endpoint_id -> session_id (ownership mapping)
        self._ownership: dict[str, str] = {}

    def create_endpoint(self, session_id: str, endpoint: WebhookEndpoint) -> None:
        if session_id not in self._endpoints:
            self._endpoints[session_id] = {}
        self._endpoints[session_id][endpoint.id] = endpoint
        self._events[endpoint.id] = deque(maxlen=_MAX_EVENTS)
        self._ownership[endpoint.id] = session_id

    def get_endpoint(self, endpoint_id: str) -> WebhookEndpoint | None:
        session_id = self._ownership.get(endpoint_id)
        if session_id and session_id in self._endpoints:
            return self._endpoints[session_id].get(endpoint_id)
        return None

    def list_endpoints(self, session_id: str) -> list[WebhookEndpoint]:
        """List endpoints only for this session."""
        if session_id not in self._endpoints:
            return []
        return list(self._endpoints[session_id].values())

    def add_event(self, event: WebhookEvent) -> None:
        if event.endpoint_id in self._events:
            self._events[event.endpoint_id].appendleft(event)
            # Update event count
            session_id = self._ownership.get(event.endpoint_id)
            if session_id and session_id in self._endpoints:
                ep = self._endpoints[session_id].get(event.endpoint_id)
                if ep:
                    self._endpoints[session_id][event.endpoint_id] = ep.model_copy(
                        update={"event_count": ep.event_count + 1}
                    )

    def get_events(self, endpoint_id: str) -> list[WebhookEvent]:
        if endpoint_id in self._events:
            return list(self._events[endpoint_id])
        return []

    def clear_events(self, endpoint_id: str) -> None:
        if endpoint_id in self._events:
            self._events[endpoint_id].clear()

    def delete_endpoint(self, endpoint_id: str) -> None:
        session_id = self._ownership.pop(endpoint_id, None)
        if session_id and session_id in self._endpoints:
            self._endpoints[session_id].pop(endpoint_id, None)
        self._events.pop(endpoint_id, None)

    def endpoint_exists(self, endpoint_id: str) -> bool:
        return endpoint_id in self._ownership

    def is_owner(self, session_id: str, endpoint_id: str) -> bool:
        """Check if a session owns an endpoint."""
        return self._ownership.get(endpoint_id) == session_id


# Singleton instance
webhook_store = WebhookStore()
