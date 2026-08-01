import streamlit as st

from components.sidebar import render_sidebar
from utils.analytics import (
    get_winner,
    fastest_lap,
    biggest_gainer,
    biggest_loser,
)

st.set_page_config(
    page_title="AI Race Insights",
    page_icon="🤖",
    layout="wide",
)

session, year, event, session_name = render_sidebar()

results = session.results
laps = session.laps

winner = get_winner(results)
fastest = fastest_lap(laps)
gainer = biggest_gainer(results)
loser = biggest_loser(results)

st.title("🤖 AI Race Insights")
st.caption(f"{event} • {year} • {session_name}")

st.divider()

st.info(
    "These insights are generated automatically from the race data."
)

insights = [

    f"""
🏆 **Winner**

{winner['FullName']} won the race for **{winner['TeamName']}** after starting from P{int(winner['GridPosition'])}.
""",

    f"""
⚡ **Fastest Lap**

{fastest['Driver']} recorded the fastest lap of the race in **{fastest['LapTime']}**.
""",

    f"""
📈 **Biggest Gainer**

{gainer['FullName']} gained **{int(gainer['Change'])} positions** during the race.
""",

    f"""
📉 **Biggest Loser**

{loser['FullName']} lost **{abs(int(loser['Change']))} positions** during the race.
""",

]

for insight in insights:

    st.markdown(insight)

    st.divider()

st.subheader("Race Statistics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Drivers",
        len(results)
    )

with c2:
    st.metric(
        "Finishers",
        len(results[results["Status"] == "Finished"])
    )

with c3:
    st.metric(
        "Total Points",
        int(results["Points"].sum())
    )

st.divider()

st.caption(
    "RaceIntel v1.0 • Built with Python, Streamlit, FastF1, Plotly and Pandas"
)