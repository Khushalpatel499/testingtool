"""Request builder component - builds the API request form."""

import json
import streamlit as st
from frontend.utils.ui_helpers import parse_curl

HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
AUTH_TYPES = ["None", "Bearer Token", "Basic Auth", "API Key"]


def render_request_builder() -> dict | None:
    """Render the request builder form. Returns request payload on submit, else None."""

    # cURL import
    with st.expander("📋 Import cURL"):
        curl_input = st.text_area("Paste cURL command", key="curl_input", height=80)
        if st.button("Import", key="import_curl"):
            if curl_input.strip():
                parsed = parse_curl(curl_input)
                st.session_state["req_url"] = parsed["url"]
                st.session_state["req_method"] = parsed["method"]
                st.session_state["req_headers_text"] = json.dumps(parsed["headers"], indent=2) if parsed["headers"] else "{}"
                st.session_state["req_body"] = parsed["body"] or ""
                st.rerun()

    # Method + URL row
    col1, col2 = st.columns([1, 5])
    with col1:
        method = st.selectbox("Method", HTTP_METHODS, key="req_method")
    with col2:
        url = st.text_input("URL", placeholder="https://api.example.com/endpoint", key="req_url")

    # Tabs for params, headers, body, auth
    tab_params, tab_headers, tab_body, tab_auth = st.tabs(
        ["Query Params", "Headers", "Body", "Auth"]
    )

    with tab_params:
        params_text = st.text_area(
            "Query Parameters (JSON object)",
            value='{}',
            height=100,
            key="req_params",
            help='Example: {"key": "value", "page": "1"}',
        )

    with tab_headers:
        # Use req_headers_text from cURL import if available
        default_headers = st.session_state.pop("req_headers_text", None)
        if default_headers:
            st.session_state["req_headers"] = default_headers
        headers_text = st.text_area(
            "Headers (JSON object)",
            height=100,
            key="req_headers",
            help='Example: {"Content-Type": "application/json"}',
        )
        if not headers_text:
            headers_text = '{}'

    with tab_body:
        # Use req_body from cURL import if available
        default_body = st.session_state.pop("req_body", None)
        if default_body:
            st.session_state["req_body_input"] = default_body
        body = st.text_area(
            "Request Body",
            height=200,
            key="req_body_input",
            help="Raw JSON or text body",
        )
        # JSON validation indicator
        if body.strip():
            try:
                json.loads(body)
                st.caption("✅ Valid JSON")
            except json.JSONDecodeError:
                st.caption("ℹ️ Not JSON (will be sent as raw text)")

    with tab_auth:
        auth_type = st.selectbox("Auth Type", AUTH_TYPES, key="req_auth_type")
        auth_value = None
        if auth_type == "Bearer Token":
            auth_value = st.text_input("Token", type="password", key="auth_token")
        elif auth_type == "Basic Auth":
            auth_value = st.text_input(
                "Credentials", placeholder="username:password", type="password", key="auth_basic"
            )
        elif auth_type == "API Key":
            auth_value = st.text_input(
                "API Key", placeholder="X-API-Key:your-key-here", type="password", key="auth_apikey"
            )

    # Action buttons
    col_send, col_clear = st.columns([1, 1])
    with col_send:
        send_clicked = st.button("🚀 Send Request", type="primary", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            for key in ["req_url", "req_body_input", "req_params", "req_headers"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    if send_clicked:
        if not url:
            st.error("Please enter a URL")
            return None

        # Parse headers and params
        try:
            headers = json.loads(headers_text) if headers_text.strip() else {}
        except json.JSONDecodeError:
            st.error("Invalid JSON in Headers")
            return None

        try:
            params = json.loads(params_text) if params_text.strip() else {}
        except json.JSONDecodeError:
            st.error("Invalid JSON in Query Params")
            return None

        return {
            "method": method,
            "url": url,
            "headers": headers,
            "params": params,
            "body": body if body.strip() else None,
            "auth_type": auth_type,
            "auth_value": auth_value,
            "timeout": 30.0,
        }

    return None
