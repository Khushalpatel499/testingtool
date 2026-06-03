"""User-Agent parser — extracts device and browser info from UA string."""

import re


def parse_user_agent(ua: str) -> str:
    """Parse User-Agent string into a human-readable device/browser summary."""
    if not ua:
        return "Unknown"

    # Common libraries/tools
    tool_patterns = [
        (r"curl/[\d.]+", "cURL"),
        (r"python-requests/([\d.]+)", "Python Requests {0}"),
        (r"python-httpx/([\d.]+)", "Python HTTPX {0}"),
        (r"axios/([\d.]+)", "Axios {0}"),
        (r"node-fetch", "Node.js Fetch"),
        (r"Go-http-client", "Go HTTP Client"),
        (r"Java/([\d.]+)", "Java {0}"),
        (r"okhttp/([\d.]+)", "OkHttp {0}"),
        (r"PostmanRuntime", "Postman"),
        (r"insomnia/([\d.]+)", "Insomnia {0}"),
        (r"wget", "Wget"),
        (r"httpie", "HTTPie"),
    ]

    for pattern, label in tool_patterns:
        match = re.search(pattern, ua, re.IGNORECASE)
        if match:
            groups = match.groups()
            return label.format(*groups) if groups else label

    # Browser detection
    browser = "Unknown Browser"
    if "Edg/" in ua:
        ver = re.search(r"Edg/([\d.]+)", ua)
        browser = f"Edge {ver.group(1).split('.')[0]}" if ver else "Edge"
    elif "Chrome/" in ua and "Safari/" in ua:
        ver = re.search(r"Chrome/([\d.]+)", ua)
        browser = f"Chrome {ver.group(1).split('.')[0]}" if ver else "Chrome"
    elif "Firefox/" in ua:
        ver = re.search(r"Firefox/([\d.]+)", ua)
        browser = f"Firefox {ver.group(1).split('.')[0]}" if ver else "Firefox"
    elif "Safari/" in ua and "Chrome/" not in ua:
        ver = re.search(r"Version/([\d.]+)", ua)
        browser = f"Safari {ver.group(1).split('.')[0]}" if ver else "Safari"

    # OS detection
    os_name = "Unknown OS"
    if "Windows NT 10" in ua:
        os_name = "Windows 10/11"
    elif "Windows NT" in ua:
        os_name = "Windows"
    elif "Mac OS X" in ua:
        os_name = "macOS"
    elif "Linux" in ua and "Android" not in ua:
        os_name = "Linux"
    elif "Android" in ua:
        ver = re.search(r"Android ([\d.]+)", ua)
        os_name = f"Android {ver.group(1)}" if ver else "Android"
    elif "iPhone" in ua or "iPad" in ua:
        os_name = "iOS"

    return f"{browser} on {os_name}"
