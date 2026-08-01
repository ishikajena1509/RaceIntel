"""
=========================================================
RaceIntel
Sidebar Component
=========================================================
"""

import streamlit as st

from utils.data_loader import (
    get_schedule,
    load_session,
)


def render_sidebar():
    """Shared sidebar for all RaceIntel pages."""

    with st.sidebar:

        st.title("🏎 RaceIntel")
        st.markdown("---")

        current_year = 2026

        year = st.selectbox(
            "Season",
            list(range(current_year, 2018, -1)),
        )

        schedule = get_schedule(year)
        events = schedule["EventName"].tolist()

        event = st.selectbox(
            "Grand Prix",
            events,
        )

        session_name = st.selectbox(
            "Session",
            [
                "Practice 1",
                "Practice 2",
                "Practice 3",
                "Sprint Qualifying",
                "Sprint",
                "Qualifying",
                "Race",
            ],
            index=6,
        )

        st.markdown("---")

        load = st.button(
            "🚀 Load Session",
            use_container_width=True,
        )


    if load:

        with st.spinner("Loading session..."):

            session = load_session(
                year,
                event,
                session_name,
            )

            st.session_state["session"] = session
            st.session_state["year"] = year
            st.session_state["event"] = event
            st.session_state["session_name"] = session_name


    if "session" not in st.session_state:

        st.info(
            "Select a season, Grand Prix and session then press **Load Session**."
        )

        st.stop()

    return (
        st.session_state["session"],
        st.session_state["year"],
        st.session_state["event"],
        st.session_state["session_name"],
    )