"""In-memory storage for API request history — session-based."""

from collections import deque
from backend.models.request_models import OutgoingRequest, OutgoingResponse

_MAX_HISTORY = 50


class HistoryEntry:
    """A single history entry pairing request with response."""

    def __init__(self, request: OutgoingRequest, response: OutgoingResponse) -> None:
        self.request = request
        self.response = response


class HistoryStore:
    """Session-based in-memory store for API test request history."""

    def __init__(self) -> None:
        # session_id -> deque of HistoryEntry
        self._sessions: dict[str, deque[HistoryEntry]] = {}

    def _get_session(self, session_id: str) -> deque[HistoryEntry]:
        if session_id not in self._sessions:
            self._sessions[session_id] = deque(maxlen=_MAX_HISTORY)
        return self._sessions[session_id]

    def add(self, session_id: str, request: OutgoingRequest, response: OutgoingResponse) -> None:
        self._get_session(session_id).appendleft(HistoryEntry(request, response))

    def get_all(self, session_id: str) -> list[dict]:
        return [
            {
                "request": entry.request.model_dump(),
                "response": entry.response.model_dump(),
            }
            for entry in self._get_session(session_id)
        ]

    def clear(self, session_id: str) -> None:
        if session_id in self._sessions:
            self._sessions[session_id].clear()


# Singleton instance
history_store = HistoryStore()
