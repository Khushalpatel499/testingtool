"""UI utility helpers for Streamlit frontend."""

import json
from typing import Any


def format_json(data: Any) -> str:
    """Pretty-format JSON data."""
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return data
    return json.dumps(data, indent=2, ensure_ascii=False)


def status_color(code: int) -> str:
    """Return a color indicator based on HTTP status code."""
    if 200 <= code < 300:
        return "🟢"
    elif 300 <= code < 400:
        return "🟡"
    elif 400 <= code < 500:
        return "🟠"
    elif code >= 500:
        return "🔴"
    return "⚪"


def parse_curl(curl_command: str) -> dict:
    """Parse a cURL command into request components."""
    import shlex
    result = {"method": "GET", "url": "", "headers": {}, "body": None}

    # Normalize line continuations and parse respecting quotes
    cleaned = curl_command.replace("\\\n", " ").replace("\\\r\n", " ").strip()
    try:
        parts = shlex.split(cleaned)
    except ValueError:
        # Fallback if shlex fails
        parts = cleaned.split()

    i = 0
    while i < len(parts):
        part = parts[i]
        if part.lower() == "curl":
            i += 1
            continue
        elif part == "-X" and i + 1 < len(parts):
            result["method"] = parts[i + 1].upper()
            i += 2
        elif part in ("-H", "--header") and i + 1 < len(parts):
            header = parts[i + 1]
            if ":" in header:
                key, val = header.split(":", 1)
                result["headers"][key.strip()] = val.strip()
            i += 2
        elif part in ("-d", "--data", "--data-raw") and i + 1 < len(parts):
            result["body"] = parts[i + 1]
            if result["method"] == "GET":
                result["method"] = "POST"
            i += 2
        elif part == "--location":
            # Follow redirects flag, skip
            i += 1
        elif part.startswith("http"):
            result["url"] = part
            i += 1
        else:
            if not result["url"] and not part.startswith("-"):
                result["url"] = part
            i += 1

    return result
