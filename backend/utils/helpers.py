"""Backend utility helpers."""


def truncate_string(s: str, max_length: int = 10000) -> str:
    """Truncate a string to max_length characters."""
    if len(s) > max_length:
        return s[:max_length] + "... [truncated]"
    return s
