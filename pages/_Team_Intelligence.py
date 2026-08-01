import streamlit as st
import plotly.express as px

from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Team Intelligence",
    page_icon="🏁",
    layout="wide",
)

session, year, event, session_name = render_sidebar()

results = session.results

st.title("🏁 Team Intelligence")
st.caption(f"{event} • {year} • {session_name}")

st.divider()


team_summary = (
    results.groupby("TeamName")
    .agg(
        Drivers=("DriverNumber", "count"),
        Points=("Points", "sum"),
        BestFinish=("Position", "min"),
        AverageFinish=("Position", "mean"),
    )
    .reset_index()
    .sort_values("Points", ascending=False)
)


c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Teams",
        len(team_summary)
    )

with c2:
    st.metric(
        "Winning Team",
        results.sort_values("Position").iloc[0]["TeamName"]
    )

with c3:
    st.metric(
        "Total Points",
        int(results["Points"].sum())
    )

st.divider()

fig = px.bar(
    team_summary,
    x="TeamName",
    y="Points",
    color="Points",
    text="Points",
    template="plotly_dark",
    title="Constructor Points"
)

fig.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Points",
    showlegend=False,
)

st.plotly_chart(
    fig,
    use_container_width=True
)


fig2 = px.bar(
    team_summary,
    x="TeamName",
    y="BestFinish",
    color="BestFinish",
    text="BestFinish",
    template="plotly_dark",
    title="Best Race Finish"
)

fig2.update_yaxes(
    autorange="reversed"
)

fig2.update_layout(
    height=450,
    showlegend=False,
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


st.subheader("Team Statistics")

st.dataframe(
    team_summary,
    use_container_width=True,
    hide_index=True,
)
st.caption(
    "RaceIntel v1.0 • Built with Python, Streamlit, FastF1, Plotly and Pandas"
)