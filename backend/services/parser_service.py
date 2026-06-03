"""Parser service - detects content type and delegates to appropriate parser."""

from typing import Any, Optional

from backend.parsers.json_parser import parse_json
from backend.parsers.form_parser import parse_form
from backend.parsers.xml_parser import parse_xml
from backend.parsers.raw_parser import parse_raw


def parse_body(content_type: Optional[str], raw_body: str) -> Optional[Any]:
    """Parse raw body based on content-type header. Never assumes JSON."""
    if not raw_body:
        return None

    ct = (content_type or "").lower()

    if "application/json" in ct:
        return parse_json(raw_body)
    elif "application/x-www-form-urlencoded" in ct:
        return parse_form(raw_body)
    elif "application/xml" in ct or "text/xml" in ct:
        return parse_xml(raw_body)
    elif "text/plain" in ct:
        return parse_raw(raw_body)
    else:
        # Try JSON as a best-effort fallback, but keep raw available
        result = parse_json(raw_body)
        return result if result is not None else raw_body
