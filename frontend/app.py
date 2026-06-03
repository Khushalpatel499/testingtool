"""Streamlit application entry point."""

import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

st.set_page_config(
    page_title="DevTool - API & Webhook Tester",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Clean UI styling
st.markdown("""
<style>
    .stTextInput > div > div > input { font-family: 'JetBrains Mono', monospace; }
    .stTextArea > div > div > textarea { font-family: 'JetBrains Mono', monospace; }
    .stCode { border-radius: 8px; }
    div[data-testid="stExpander"] { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🛠️ DevTool")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        options=["🚀 API Tester", "🪝 Webhook Tester"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Built with Streamlit + FastAPI")

# Route to selected page
if page == "🚀 API Tester":
    from frontend.components.request_builder import render_request_builder
    from frontend.components.response_viewer import render_response_viewer
    from frontend.services.backend_client import send_api_request, get_history, clear_history
    from frontend.utils.ui_helpers import status_color

    st.markdown("## 🚀 API Tester")
    st.caption("Send HTTP requests and inspect responses — like Postman, in your browser.")

    col_req, col_resp = st.columns([1, 1])

    with col_req:
        st.markdown("#### Request")
        payload = render_request_builder()

    if payload:
        with st.spinner("Sending request..."):
            try:
                response = send_api_request(payload)
                st.session_state["last_response"] = response
            except Exception as e:
                st.session_state["last_response"] = {
                    "status_code": 0, "headers": {}, "body": "",
                    "elapsed_ms": 0, "error": f"Backend connection failed: {e}",
                }

    with col_resp:
        st.markdown("#### Response")
        render_response_viewer(st.session_state.get("last_response"))

    st.markdown("---")
    st.markdown("#### 📜 Request History")
    col_refresh, col_clear = st.columns([1, 1])
    with col_refresh:
        if st.button("🔄 Refresh History"):
            st.session_state["history"] = get_history()
    with col_clear:
        if st.button("🗑️ Clear History"):
            clear_history()
            st.session_state["history"] = []

    history = st.session_state.get("history", [])
    if history:
        for entry in history[:10]:
            req = entry["request"]
            resp = entry["response"]
            badge = status_color(resp["status_code"])
            st.markdown(f"{badge} **{req['method']}** `{req['url']}` → {resp['status_code']} ({resp['elapsed_ms']:.0f}ms)")
    else:
        st.caption("No history yet. Send a request to see it here.")

elif page == "🪝 Webhook Tester":
    from frontend.services.backend_client import (
        create_webhook_endpoint,
        list_webhook_endpoints,
        get_webhook_events,
        clear_webhook_events,
        delete_webhook_endpoint,
    )
    from frontend.components.webhook_viewer import render_webhook_viewer

    st.markdown("## 🪝 Webhook Tester")
    st.caption("Generate webhook URLs, send requests from anywhere, and inspect them live.")

    # Only create when user explicitly clicks
    if st.button("➕ Create New Webhook Endpoint", type="primary"):
        try:
            ep = create_webhook_endpoint()
            st.session_state["webhook_just_created"] = ep["url"]
        except Exception as e:
            st.error(f"Failed to create endpoint: {e}")

    if "webhook_just_created" in st.session_state:
        st.success(f"Created: `{st.session_state['webhook_just_created']}`")
        del st.session_state["webhook_just_created"]

    st.markdown("---")

    # List endpoints
    try:
        endpoints = list_webhook_endpoints()
    except Exception:
        st.error("Cannot connect to backend. Make sure the backend is running.")
        endpoints = None

    if endpoints is not None:
        if not endpoints:
            st.info("No webhook endpoints yet. Create one above.")
        else:
            endpoint_options = {ep["id"]: ep for ep in endpoints}
            selected_id = st.selectbox(
                "Select Endpoint",
                options=list(endpoint_options.keys()),
                format_func=lambda x: f"{endpoint_options[x]['url']} ({endpoint_options[x]['event_count']} events)",
            )

            if selected_id:
                ep = endpoint_options[selected_id]
                st.code(ep["url"], language="text")
                st.caption(f"Created: {ep['created_at']} | Events: {ep['event_count']}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔄 Refresh Events"):
                        st.rerun()
                with col2:
                    if st.button("🗑️ Clear Events"):
                        clear_webhook_events(selected_id)
                        st.rerun()
                with col3:
                    if st.button("❌ Delete Endpoint"):
                        delete_webhook_endpoint(selected_id)
                        st.rerun()

                events = get_webhook_events(selected_id)
                render_webhook_viewer(events)
