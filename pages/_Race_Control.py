import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Race Control",
    page_icon="🚦",
    layout="wide",
)
session, year, event, session_name = render_sidebar()

race_control = session.race_control_messages
track_status = session.track_status

st.title("🚦 Race Control")

st.caption(f"{event} • {year} • {session_name}")

st.divider()

yellow_flags = len(
    race_control[
        race_control["Message"].str.contains(
            "YELLOW",
            case=False,
            na=False,
        )
    ]
)

safety_car = len(
    race_control[
        race_control["Message"].str.contains(
            "SAFETY CAR",
            case=False,
            na=False,
        )
    ]
)

red_flags = len(
    race_control[
        race_control["Message"].str.contains(
            "RED",
            case=False,
            na=False,
        )
    ]
)

messages = len(race_control)

c1, c2, c3, c4 = st.columns(4)

c1.metric("🟡 Yellow Flags", yellow_flags)
c2.metric("🚗 Safety Cars", safety_car)
c3.metric("🔴 Red Flags", red_flags)
c4.metric("📢 Messages", messages)

st.divider()

st.subheader("📊 Event Distribution")

category_counts = (
    race_control["Category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = ["Category", "Count"]

fig = px.pie(
    category_counts,
    names="Category",
    values="Count",
    hole=0.45,
    template="plotly_dark",
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True,
)


st.subheader("🏁 Track Status Timeline")

status_map = {
    "1": "Green",
    "2": "Yellow",
    "4": "Safety Car",
    "5": "Red Flag",
    "6": "VSC",
    "7": "VSC Ending",
}

timeline = track_status.copy()

timeline["StatusName"] = (
    timeline["Status"]
    .astype(str)
    .map(status_map)
    .fillna("Other")
)

fig2 = px.scatter(
    timeline,
    x="Time",
    y="StatusName",
    color="StatusName",
    template="plotly_dark",
)

fig2.update_layout(
    height=450,
    xaxis_title="Session Time",
    yaxis_title="Track Status",
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

st.subheader("📋 Race Control Feed")

display = race_control.copy()

columns = [
    "Time",
    "Category",
    "Message",
]

if "Lap" in display.columns:
    columns.append("Lap")

display = display[columns]

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
)

st.success("✅ Race Control page loaded successfully.")

st.caption(
    "RaceIntel v1.0 • Built with Python, Streamlit, FastF1, Plotly and Pandas"
)