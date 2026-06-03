"""Response viewer component - displays API response data."""

import json
import streamlit as st
from frontend.utils.ui_helpers import format_json, status_color


def render_response_viewer(response: dict | None) -> None:
    """Render the response viewer panel."""
    if response is None:
        st.info("Send a request to see the response here.")
        return

    # Error state
    if response.get("error"):
        st.error(f"❌ Error: {response['error']}")
        return

    status = response["status_code"]
    elapsed = response["elapsed_ms"]

    # Status bar
    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown(f"### {status_color(status)} Status: **{status}**")
    with col2:
        st.markdown(f"### ⏱️ Time: **{elapsed:.0f} ms**")

    st.markdown("---")

    # Response tabs
    tab_body, tab_headers, tab_raw = st.tabs(["Body", "Headers", "Raw"])

    with tab_body:
        body = response.get("body", "")
        # Try to pretty-print JSON
        try:
            parsed = json.loads(body)
            st.code(format_json(parsed), language="json")
        except (json.JSONDecodeError, TypeError):
            st.code(body, language="text")

        # Copy button
        if body:
            st.button("📋 Copy Response", key="copy_resp",
                     on_click=lambda: st.session_state.update({"_clipboard": body}))

    with tab_headers:
        headers = response.get("headers", {})
        if headers:
            st.json(headers)
        else:
            st.caption("No headers")

    with tab_raw:
        st.code(response.get("body", ""), language="text")
