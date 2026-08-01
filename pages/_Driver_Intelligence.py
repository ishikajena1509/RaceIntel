import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from components.sidebar import render_sidebar
from pages._Dashboard import format_lap_time

st.set_page_config(
    page_title="Driver Intelligence",
    page_icon="👤",
    layout="wide",
)

session, year, event, session_name = render_sidebar()

results = session.results
laps = session.laps

st.title("👤 Driver Intelligence")

st.caption(
    f"{event} • {year} • {session_name}"
)

st.divider()


drivers = sorted(results["Abbreviation"].tolist())

selected_driver = st.selectbox(
    "Select Driver",
    drivers,
)


driver_result = results[
    results["Abbreviation"] == selected_driver
].iloc[0]

driver_laps = laps[
    laps["Driver"] == selected_driver
].copy()

valid_laps = driver_laps.dropna(subset=["LapTime"])

fastest_lap = (
    valid_laps["LapTime"].min()
    if not valid_laps.empty
    else None
)

average_lap = (
    valid_laps["LapTime"].mean()
    if not valid_laps.empty
    else None
)

total_laps = (
    len(valid_laps)
)


st.subheader(
    f"{driver_result['FullName']}"
)

st.caption(
    driver_result["TeamName"]
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Finish Position",
        f"P{driver_result['Position']}"
    )

with col2:

    st.metric(
        "Grid Position",
        f"P{driver_result['GridPosition']}"
    )

with col3:

    st.metric(
        "Points",
        driver_result["Points"]
    )

with col4:

    st.metric(
        "Completed Laps",
        total_laps
    )

st.divider()

c1, c2 = st.columns(2)
def format_lap_time(td):
    if td is None or pd.isna(td):
        return "-"

    total_seconds = td.total_seconds()

    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:06.3f}"
with c1:
    st.metric(
        "Fastest Lap",
        format_lap_time(fastest_lap)
    )

with c2:

    st.metric(
        "Average Lap",
        format_lap_time(average_lap)
    )

st.divider()

if not valid_laps.empty:

    fastest = valid_laps.loc[
        valid_laps["LapTime"].idxmin()
    ]

    telemetry = fastest.get_car_data().add_distance()


    st.subheader("🚀 Speed Trace")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=telemetry["Distance"],
            y=telemetry["Speed"],
            mode="lines",
            line=dict(
                color="#00D2BE",
                width=3,
            ),
            name="Speed",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=350,
        xaxis_title="Distance (m)",
        yaxis_title="Speed (km/h)",
    )

    st.plotly_chart(fig, use_container_width=True)



    st.subheader("🟢 Throttle")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=telemetry["Distance"],
            y=telemetry["Throttle"],
            mode="lines",
            line=dict(
                color="#00C853",
                width=3,
            ),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=320,
        xaxis_title="Distance (m)",
        yaxis_title="Throttle %",
    )

    st.plotly_chart(fig, use_container_width=True)



    st.subheader("🔴 Brake")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=telemetry["Distance"],
            y=telemetry["Brake"],
            mode="lines",
            line=dict(
                color="#E53935",
                width=3,
            ),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=320,
        xaxis_title="Distance (m)",
        yaxis_title="Brake",
    )

    st.plotly_chart(fig, use_container_width=True)



    st.subheader("⚙ Engine RPM")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=telemetry["Distance"],
            y=telemetry["RPM"],
            mode="lines",
            line=dict(
                color="#FF9800",
                width=3,
            ),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=320,
        xaxis_title="Distance (m)",
        yaxis_title="RPM",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("⚙ Gear Changes")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=telemetry["Distance"],
            y=telemetry["nGear"],
            mode="lines",
            line=dict(
                color="#2979FF",
                width=3,
            ),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=320,
        xaxis_title="Distance (m)",
        yaxis_title="Gear",
    )

    st.plotly_chart(fig, use_container_width=True)

else:

    st.warning(
        "No telemetry available for this driver."
    )

import plotly.express as px

st.divider()
st.subheader("📈 Lap Time Trend")

lap_data = valid_laps.copy()

lap_data["LapSeconds"] = lap_data["LapTime"].dt.total_seconds()

fig = px.line(
    lap_data,
    x="LapNumber",
    y="LapSeconds",
    template="plotly_dark",
    markers=True,
)

fig.update_layout(
    height=350,
    xaxis_title="Lap",
    yaxis_title="Lap Time (s)",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


st.divider()
st.subheader("🛞 Tyre Usage")

compound_summary = (
    driver_laps.groupby("Compound")
    .size()
    .reset_index(name="Laps")
)

fig = px.pie(
    compound_summary,
    names="Compound",
    values="Laps",
    hole=0.45,
    template="plotly_dark",
)

fig.update_layout(
    height=400,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()
st.subheader("📋 Lap Summary")

table = driver_laps[
    [
        "LapNumber",
        "LapTime",
        "Compound",
        "TyreLife",
        "SpeedST",
        "Sector1Time",
        "Sector2Time",
        "Sector3Time",
    ]
].copy()

table["LapTime"] = table["LapTime"].apply(format_lap_time)
table["Sector1Time"] = table["Sector1Time"].apply(format_lap_time)
table["Sector2Time"] = table["Sector2Time"].apply(format_lap_time)
table["Sector3Time"] = table["Sector3Time"].apply(format_lap_time)

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
)
st.caption(
    "RaceIntel v1.0 • Built with Python, Streamlit, FastF1, Plotly and Pandas"
)