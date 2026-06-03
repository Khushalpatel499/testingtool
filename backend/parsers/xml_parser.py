"""XML body parser."""

from typing import Optional
import xml.etree.ElementTree as ET


def parse_xml(raw_body: str) -> Optional[str]:
    """Validate and return XML string. Returns None if invalid XML."""
    try:
        ET.fromstring(raw_body)
        return raw_body  # Return raw XML string if valid
    except (ET.ParseError, TypeError):
        return None
