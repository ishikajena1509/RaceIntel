import streamlit as st
from components.cards import metric_card
from components.podium import podium_card
from utils.charts import position_change_chart
from components.insight_cards import insight_card
from utils.theme import get_team_color
from components.sidebar import render_sidebar
from utils.analytics import (
    dashboard_cards,
    get_winner,
    fastest_lap,
    biggest_gainer,
    biggest_loser,
    pole_sitter,
)
def format_lap_time(td):

    if td is None:
        return "-"

    seconds = td.total_seconds()

    minutes = int(seconds // 60)

    seconds = seconds % 60

    return f"{minutes}:{seconds:06.3f}"



st.set_page_config(
    page_title="RaceIntel Dashboard",
    page_icon="🏎",
    layout="wide",
)


session, year, event, session_name = render_sidebar()

results = session.results
laps = session.laps
weather = session.weather_data


st.markdown(
    f"""
# 🏎 RaceIntel

### {event}

**{session_name} • {year}**
"""
)


cards = dashboard_cards(
    results,
    laps,
    weather,
)

winner = get_winner(results)
fastest = fastest_lap(laps)

col1, col2, col3, col4 = st.columns(4)

with col1:

    metric_card(
        title="Winner",
        value=winner["FullName"] if winner is not None else "-",
        icon="🏆",
        subtitle=winner["TeamName"] if winner is not None else "",
        color=get_team_color(winner["TeamName"]) if winner is not None else "#FFD700"
    )

with col2:

    metric_card(
        title="Fastest Lap",
        value=fastest["Driver"] if fastest is not None else "-",
        icon="⚡",
        subtitle=format_lap_time(fastest["LapTime"]) if fastest is not None else "",
        color="#00C853",
    )

with col3:

    metric_card(
        title="Drivers",
        value=cards["Drivers"],
        icon="👥",
        subtitle="Classified Drivers",
        color="#2979FF",
    )

with col4:

    track_temp = (
        "-"
        if cards["Track Temp"] is None
        else f"{cards['Track Temp']} °C"
    )

    metric_card(
        title="Track Temperature",
        value=track_temp,
        icon="🌡",
        subtitle="Average Track Temp",
        color="#FF6D00",
    )
st.divider()

st.subheader("🥇 Race Podium")
podium = results.sort_values("Position").head(3)

silver = podium.iloc[1]
gold = podium.iloc[0]
bronze = podium.iloc[2]

col1, col2, col3 = st.columns(
    [1, 1.2, 1],
    vertical_alignment="bottom",
)

with col1:
    podium_card(
        "🥈",
        silver["FullName"],
        silver["TeamName"],
        get_team_color(silver["TeamName"]),
    )

with col2:
    podium_card(
        "🥇",
        gold["FullName"],
        gold["TeamName"],
        get_team_color(gold["TeamName"]),
    )

with col3:
    podium_card(
        "🥉",
        bronze["FullName"],
        bronze["TeamName"],
        get_team_color(bronze["TeamName"]),
    )
st.divider()

st.subheader("📈 Position Changes")

fig = position_change_chart(results)

st.plotly_chart(
    fig,
    use_container_width=True,
)
gainer = biggest_gainer(results)
loser = biggest_loser(results)
pole = pole_sitter(results)
fastest = fastest_lap(laps)
st.divider()

st.subheader("📋 Race Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    insight_card(
        title="Biggest Gainer",
        value=gainer["FullName"],
        subtitle=f"▲ +{int(gainer['Change'])} Positions",
        color="#00C853",
        icon="📈",
    )

with col2:
    insight_card(
        title="Biggest Loser",
        value=loser["FullName"],
        subtitle=f"▼ {abs(int(loser['Change']))} Positions",
        color="#E53935",
        icon="📉",
    )

with col3:
    insight_card(
        title="Pole Sitter",
        value=pole["FullName"],
        subtitle=f"{pole['TeamName']}",
        color="#FFD700",
        icon="🏁",
    )

with col4:
    insight_card(
        title="Fastest Lap",
        value=fastest["Driver"],
        subtitle=format_lap_time(fastest["LapTime"]),
        color="#00D2BE",
        icon="⚡",
    )
st.caption(
    "RaceIntel v1.0 • Built with Python, Streamlit, FastF1, Plotly and Pandas"
)