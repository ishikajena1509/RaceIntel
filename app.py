import streamlit as st

st.set_page_config(
    page_title="RaceIntel",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    with open("assets/styles.css", "r", encoding="utf-8") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("styles.css not found. Using default Streamlit styling.")

st.title("🏎️ RaceIntel")
st.subheader("Formula One Race Intelligence Platform")

st.markdown(
    """
RaceIntel is a Formula One analytics platform built using **FastF1**, **Streamlit**,
**Pandas**, and **Plotly**. It provides race engineers, analysts, and fans with
interactive insights into Formula 1 sessions.

### 🚀 Key Features
- 📊 Race Dashboard
- 👤 Driver Intelligence
- 🏎️ Team Intelligence
- 🛞 Strategy Simulator
- 🚨 Race Control Monitor
- 🤖 AI Race Engineer

Use the navigation menu on the left to explore each module.
"""
)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
### 📈 Analytics
Compare drivers, teams, lap times,
positions, tyre strategies, and
performance trends.
"""
    )

with col2:
    st.success(
        """
### 🧠 AI Insights
Generate automated race summaries,
strategy observations, and key
performance highlights.
"""
    )

with col3:
    st.warning(
        """
### 🏁 Strategy
Simulate pit stop decisions using
lap number, tyre age, and
race context.
"""
    )

st.divider()

st.markdown("## ✨ Why RaceIntel?")

left, right = st.columns([2, 1])

with left:
    st.markdown(
        """
RaceIntel is designed as a portfolio-ready Formula One analytics application.

It demonstrates:

- Python application development
- Sports data analytics
- FastF1 data processing
- Interactive data visualization
- Decision-support systems
- Modular software architecture
"""
    )

with right:
    st.metric("Framework", "Streamlit")
    st.metric("Data Source", "FastF1")
    st.metric("Charts", "Plotly")

st.divider()


st.caption(
    "RaceIntel v1.0 • Built with Python, Streamlit, FastF1, Plotly and Pandas"
)