import streamlit as st
import plotly.express as px

from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Strategy Centre",
    page_icon="🛞",
    layout="wide",
)

session, year, event, session_name = render_sidebar()

laps = session.laps

st.title("🛞 Strategy Centre")
st.caption(f"{event} • {year} • {session_name}")

st.divider()

st.subheader("Tyre Strategy")

stints = (
    laps.groupby(["Driver", "Stint", "Compound"])
    .agg(
        StartLap=("LapNumber", "min"),
        EndLap=("LapNumber", "max"),
        Laps=("LapNumber", "count"),
    )
    .reset_index()
)

fig = px.bar(
    stints,
    x="Laps",
    y="Driver",
    color="Compound",
    orientation="h",
    hover_data=[
        "StartLap",
        "EndLap",
        "Stint",
    ],
    template="plotly_dark",
)

fig.update_layout(
    title="Tyre Stints",
    height=700,
    xaxis_title="Number of Laps",
    yaxis_title="Driver",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

compound_usage = (
    laps.groupby(
        ["Compound"]
    )
    .size()
    .reset_index(name="Laps")
)

fig2 = px.pie(
    compound_usage,
    values="Laps",
    names="Compound",
    hole=0.45,
    template="plotly_dark",
)

fig2.update_layout(
    title="Tyre Compound Usage",
    height=500,
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

st.divider()

st.subheader("Stint Summary")

st.dataframe(
    stints,
    use_container_width=True,
    hide_index=True,
)
st.caption(
    "RaceIntel v1.0 • Built with Python, Streamlit, FastF1, Plotly and Pandas"
)