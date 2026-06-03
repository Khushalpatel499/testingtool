"""Sidebar navigation component."""

import streamlit as st


def render_sidebar() -> str:
    """Render sidebar navigation and return selected page."""
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

    return page
