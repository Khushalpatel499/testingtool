"""In-memory storage for webhook endpoints and events."""

from collections import deque
from backend.models.webhook_models import WebhookEvent, WebhookEndpoint

# Max events per endpoint
_MAX_EVENTS = 100


class WebhookStore:
    """Thread-safe in-memory store for webhook endpoints and their events."""

    def __init__(self) -> None:
        # endpoint_id -> WebhookEndpoint
        self._endpoints: dict[str, WebhookEndpoint] = {}
        # endpoint_id -> deque of WebhookEvent
        self._events: dict[str, deque[WebhookEvent]] = {}

    def create_endpoint(self, endpoint: WebhookEndpoint) -> None:
        self._endpoints[endpoint.id] = endpoint
        self._events[endpoint.id] = deque(maxlen=_MAX_EVENTS)

    def get_endpoint(self, endpoint_id: str) -> WebhookEndpoint | None:
        return self._endpoints.get(endpoint_id)

    def list_endpoints(self) -> list[WebhookEndpoint]:
        return list(self._endpoints.values())

    def add_event(self, event: WebhookEvent) -> None:
        if event.endpoint_id in self._events:
            self._events[event.endpoint_id].appendleft(event)
            # Update event count
            ep = self._endpoints[event.endpoint_id]
            self._endpoints[event.endpoint_id] = ep.model_copy(
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
        self._endpoints.pop(endpoint_id, None)
        self._events.pop(endpoint_id, None)

    def endpoint_exists(self, endpoint_id: str) -> bool:
        return endpoint_id in self._endpoints


# Singleton instance
webhook_store = WebhookStore()
