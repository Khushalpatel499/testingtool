"""Form-urlencoded body parser."""

from typing import Any, Optional
from urllib.parse import parse_qs


def parse_form(raw_body: str) -> Optional[dict[str, Any]]:
    """Parse application/x-www-form-urlencoded body."""
    try:
        parsed = parse_qs(raw_body, keep_blank_values=True)
        # Flatten single-value lists
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
    except Exception:
        return None
