"""JSON body parser."""

import json
from typing import Any, Optional


def parse_json(raw_body: str) -> Optional[Any]:
    """Attempt to parse raw body as JSON. Returns None on failure."""
    try:
        return json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return None
