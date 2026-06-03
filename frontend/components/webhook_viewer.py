"""Webhook viewer component - displays captured webhook events."""

import json
import streamlit as st
from frontend.utils.ui_helpers import format_json


def render_webhook_viewer(events: list[dict]) -> None:
    """Render the webhook event list."""
    if not events:
        st.info("No webhook events captured yet. Send a request to your webhook URL.")
        return

    st.markdown(f"**{len(events)} event(s) captured**")

    for i, event in enumerate(events):
        method = event["method"]
        timestamp = event["timestamp"]
        content_type = event.get("content_type") or "unknown"

        # Color-coded method badge
        method_colors = {
            "GET": "🟢", "POST": "🔵", "PUT": "🟡",
            "PATCH": "🟠", "DELETE": "🔴", "OPTIONS": "⚪"
        }
        badge = method_colors.get(method, "⚫")

        with st.expander(
            f"{badge} **{method}** — {content_type} — {timestamp}",
            expanded=(i == 0),
        ):
            tab_body, tab_headers, tab_query, tab_raw = st.tabs(
                ["Parsed Body", "Headers", "Query Params", "Raw Body"]
            )

            with tab_body:
                parsed = event.get("parsed_body")
                if parsed and isinstance(parsed, (dict, list)):
                    st.code(format_json(parsed), language="json")
                elif parsed:
                    st.code(str(parsed), language="text")
                else:
                    st.caption("No parsed body available")

            with tab_headers:
                st.json(event.get("headers", {}))

            with tab_query:
                qp = event.get("query_params", {})
                if qp:
                    st.json(qp)
                else:
                    st.caption("No query parameters")

            with tab_raw:
                raw = event.get("raw_body", "")
                st.code(raw if raw else "(empty body)", language="text")

            # Metadata
            st.caption(
                f"📱 Device: {event.get('device_info', 'Unknown')} | "
                f"Client IP: {event.get('client_ip', 'unknown')} | "
                f"Path: {event.get('path', '')} | "
                f"ID: {event.get('id', '')}"
            )
