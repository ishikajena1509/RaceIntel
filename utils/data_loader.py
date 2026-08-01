"""
=========================================================
RaceIntel - Data Loader


Compatible with:
- FastF1 3.8.3
- Streamlit
- Python 3.14
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional
from typing import Union
import fastf1
import pandas as pd
import streamlit as st

CACHE_DIR = Path("data") / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

fastf1.Cache.enable_cache(str(CACHE_DIR))

CURRENT_YEAR = pd.Timestamp.now().year

AVAILABLE_YEARS = list(range(2018, CURRENT_YEAR + 1))

SESSION_TYPES = [
    "Practice 1",
    "Practice 2",
    "Practice 3",
    "Sprint",
    "Sprint Qualifying",
    "Sprint Shootout",
    "Qualifying",
    "Race",
]

@st.cache_resource(show_spinner=False)
def load_session(
    year: int,
    event: str,
    session_type: str,
):
    """
    Load and cache a FastF1 session.

    Parameters
    ----------
    year : int
    event : str
    session_type : str

    Returns
    -------
    fastf1.core.Session
    """

    session = fastf1.get_session(
        year,
        event,
        session_type,
    )

    session.load()

    return session

@st.cache_data(show_spinner=False)
def get_schedule(year: int) -> pd.DataFrame:
    """
    Return the official season schedule.
    """

    schedule = fastf1.get_event_schedule(year)

    return schedule.copy()


@st.cache_data(show_spinner=False)
def get_event_names(year: int) -> list[str]:
    """
    Return all event names.
    """

    schedule = get_schedule(year)

    if "EventName" not in schedule.columns:
        return []

    return schedule["EventName"].tolist()

@st.cache_data(show_spinner=False)
def get_session_info(
    year: int,
    event: str,
) -> Optional[pd.Series]:
    """
    Return metadata for one event.
    """

    schedule = get_schedule(year)

    rows = schedule.loc[
        schedule["EventName"] == event
    ]

    if rows.empty:
        return None

    return rows.iloc[0]

def get_driver_numbers(session) -> list[str]:
    """
    Return driver numbers participating
    in the loaded session.
    """

    return sorted(session.drivers)


def get_driver_info(
    session,
    driver_number: str,
) -> dict:
    """
    Return metadata for one driver.

    Example:
        get_driver_info(session, "1")
    """

    return session.get_driver(driver_number)


def get_driver_dataframe(
    session,
) -> pd.DataFrame:
    """
    Build a DataFrame containing
    all driver information.
    """

    rows = []

    for number in session.drivers:

        info = session.get_driver(number)

        rows.append(
            {
                "DriverNumber": number,
                "Abbreviation": info.get("Abbreviation"),
                "BroadcastName": info.get("BroadcastName"),
                "FullName": info.get("FullName"),
                "TeamName": info.get("TeamName"),
                "TeamColor": info.get("TeamColor"),
                "CountryCode": info.get("CountryCode"),
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.sort_values("TeamName").reset_index(drop=True)

    return df

def get_team_list(session) -> list[str]:
    """
    Return all teams in the session.
    """

    drivers = get_driver_dataframe(session)

    if drivers.empty:
        return []

    return (
        drivers["TeamName"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

def get_session_summary(session) -> dict:
    """
    Return basic information about the
    currently loaded session.
    """

    event = session.event

    return {
        "Event": event.EventName,
        "OfficialName": event.OfficialEventName,
        "Country": event.Country,
        "Location": event.Location,
        "Year": event.EventDate.year,
        "Session": session.name,
        "Drivers": len(session.drivers),
    }

def validate_session(session) -> bool:
    """
    Basic validation helper.
    """

    try:
        return (
            session is not None
            and len(session.drivers) > 0
        )
    except Exception:
        return False

@st.cache_data(show_spinner=False)
def get_results(session) -> pd.DataFrame:
    """
    Return the official classification/results for the session.

    Returns
    -------
    pandas.DataFrame
    """

    try:
        results = session.results.copy()

        if results is None:
            return pd.DataFrame()

        return results

    except Exception:
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def get_laps(session):
    """
    Return all laps.
    """

    try:
        return session.laps.copy()

    except Exception:
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def get_weather(session):
    """
    Return weather data for the session.
    """

    try:
        weather = session.weather_data.copy()

        if weather is None:
            return pd.DataFrame()

        return weather

    except Exception:
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def get_track_status(session):
    """
    Return FIA track status information.
    """

    try:
        status = session.track_status.copy()

        if status is None:
            return pd.DataFrame()

        return status

    except Exception:
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def get_race_control(session):
    """
    Return FIA Race Control messages.
    """

    try:
        messages = session.race_control_messages.copy()

        if messages is None:
            return pd.DataFrame()

        return messages

    except Exception:
        return pd.DataFrame()

def get_fastest_laps(session) -> pd.DataFrame:
    """
    Return one fastest lap per driver.
    """

    laps = get_laps(session)

    if laps.empty:
        return pd.DataFrame()

    fastest = (
        laps
        .pick_drivers(session.drivers)
        .pick_quicklaps()
        .sort_values("LapTime")
        .groupby("Driver", as_index=False)
        .first()
    )

    return fastest.reset_index(drop=True)

def get_winner(session) -> Union[str, None]:
    """
    Return winner abbreviation for Race sessions.
    """

    results = get_results(session)

    if results.empty:
        return None

    try:
        winner = (
            results
            .sort_values("Position")
            .iloc[0]
        )

        return winner["Abbreviation"]

    except Exception:
        return None

def get_podium(session) -> pd.DataFrame:
    """
    Return top three classified drivers.
    """

    results = get_results(session)

    if results.empty:
        return pd.DataFrame()

    try:
        podium = (
            results
            .sort_values("Position")
            .head(3)
            .reset_index(drop=True)
        )

        return podium

    except Exception:
        return pd.DataFrame()

def get_fastest_driver(session):
    """
    Return the fastest lap in the session.
    """

    fastest = get_fastest_laps(session)

    if fastest.empty:
        return None

    return fastest.iloc[0]

def get_position_data(session):
    """
    Return lap-by-lap positions.

    Useful for:
    - Race replay
    - Position chart
    - Driver analysis
    """

    laps = get_laps(session)

    if laps.empty:
        return pd.DataFrame()

    columns = [
        "Driver",
        "LapNumber",
        "Position"
    ]

    available = [c for c in columns if c in laps.columns]

    return laps[available].copy()

def get_tyre_data(session):
    """
    Return tyre information for every lap.
    """

    laps = get_laps(session)

    if laps.empty:
        return pd.DataFrame()

    cols = [
        "Driver",
        "LapNumber",
        "Compound",
        "TyreLife",
        "FreshTyre",
        "Stint"
    ]

    available = [c for c in cols if c in laps.columns]

    return laps[available].copy()

def get_pit_stops(session):
    """
    Estimate pit stops from stint changes.
    """

    tyres = get_tyre_data(session)

    if tyres.empty:
        return pd.DataFrame()

    pit_rows = []

    for driver, df in tyres.groupby("Driver"):

        df = df.sort_values("LapNumber")

        previous = None

        for _, row in df.iterrows():

            if previous is None:
                previous = row["Stint"]
                continue

            if row["Stint"] != previous:

                pit_rows.append(
                    {
                        "Driver": driver,
                        "Lap": row["LapNumber"],
                        "NewStint": row["Stint"],
                        "Compound": row["Compound"]
                    }
                )

                previous = row["Stint"]

    return pd.DataFrame(pit_rows)

def get_car_data(session, driver: str):
    """
    Return processed car telemetry for a driver.
    """

    laps = get_laps(session)

    if laps.empty:
        return None

    try:
        fastest = laps.pick_drivers(driver).pick_fastest()

        if fastest is None:
            return None

        return (
            fastest
            .get_car_data()
            .add_distance()
        )

    except Exception:
        return None

def get_position_trace(session, driver: str):
    """
    Return lap-by-lap position for one driver.
    """

    laps = get_laps(session)

    if laps.empty:
        return pd.DataFrame()

    try:
        df = (
            laps[laps["Driver"] == driver]
            [["LapNumber", "Position"]]
            .copy()
            .reset_index(drop=True)
        )

        return df

    except Exception:
        return pd.DataFrame()

def get_lap_times(session, driver: str):
    """
    Return lap times for one driver.
    """

    laps = get_laps(session)

    if laps.empty:
        return pd.DataFrame()

    cols = [
        "LapNumber",
        "LapTime",
        "Compound",
        "TyreLife",
        "Stint"
    ]

    cols = [c for c in cols if c in laps.columns]

    return (
        laps[laps["Driver"] == driver][cols]
        .copy()
        .reset_index(drop=True)
    )

def get_driver_statistics(session, driver: str):
    """
    Generate basic driver statistics.
    """

    laps = get_laps(session)

    if laps.empty:
        return {}

    driver_laps = laps.pick_drivers(driver)

    if driver_laps.empty:
        return {}

    stats = {}

    stats["Driver"] = driver
    stats["CompletedLaps"] = len(driver_laps)

    try:
        fastest = driver_laps.pick_fastest()
        stats["FastestLap"] = fastest["LapTime"]
    except Exception:
        stats["FastestLap"] = None

    try:
        stats["AverageLap"] = driver_laps["LapTime"].mean()
    except Exception:
        stats["AverageLap"] = None

    try:
        stats["BestSpeed"] = driver_laps["SpeedST"].max()
    except Exception:
        stats["BestSpeed"] = None

    return stats

def get_team_statistics(session, team: str):
    """
    Return all laps completed by a team.
    """

    laps = get_laps(session)

    if laps.empty:
        return pd.DataFrame()

    if "Team" not in laps.columns:
        return pd.DataFrame()

    return (
        laps[laps["Team"] == team]
        .copy()
        .reset_index(drop=True)
    )

def get_session_kpis(session):
    """
    Return dashboard KPIs.
    """

    results = get_results(session)
    laps = get_laps(session)

    return {
        "Drivers": len(session.drivers),
        "TotalLaps": len(laps),
        "Winner": get_winner(session),
        "FastestDriver": (
            get_fastest_driver(session)["Driver"]
            if get_fastest_driver(session) is not None
            else None
        ),
        "SafetyCarEvents": len(
            get_track_status(session)
        ),
        "RaceControlMessages": len(
            get_race_control(session)
        ),
        "Finishers": len(results)
    }

def session_has_data(session):
    """
    Check whether the loaded session contains usable data.
    """

    try:
        return (
            session is not None
            and hasattr(session, "laps")
            and len(session.laps) > 0
        )
    except Exception:
        return False

__all__ = [
    "AVAILABLE_YEARS",
    "SESSION_TYPES",
    "load_session",
    "get_schedule",
    "get_event_names",
    "get_session_info",
    "get_driver_numbers",
    "get_driver_info",
    "get_driver_dataframe",
    "get_team_list",
    "get_session_summary",
    "validate_session",
    "get_results",
    "get_laps",
    "get_weather",
    "get_track_status",
    "get_race_control",
    "get_fastest_laps",
    "get_winner",
    "get_podium",
    "get_fastest_driver",
    "get_position_data",
    "get_tyre_data",
    "get_pit_stops",
    "get_car_data",
    "get_position_trace",
    "get_lap_times",
    "get_driver_statistics",
    "get_team_statistics",
    "get_session_kpis",
    "session_has_data",
]