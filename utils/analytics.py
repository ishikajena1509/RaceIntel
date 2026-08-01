"""
=========================================================
RaceIntel - Analytics

Compatible with:
- FastF1 3.8.3
- Pandas
=========================================================
"""

from __future__ import annotations
import numpy as np
import pandas as pd

def calculate_session_kpis(results: pd.DataFrame,
                           laps: pd.DataFrame,
                           weather: pd.DataFrame) -> dict:
    """
    Generate dashboard KPI values.
    """

    kpis = {
        "Drivers": 0,
        "Finishers": 0,
        "TotalLaps": 0,
        "AverageTrackTemp": None,
        "AverageAirTemp": None,
    }

    if not results.empty:

        kpis["Drivers"] = len(results)
        kpis["Finishers"] = len(
            results[
                results["ClassifiedPosition"] != "R"
            ]
        )

    if not laps.empty:
        kpis["TotalLaps"] = int(laps["LapNumber"].max())

    if not weather.empty:

        if "TrackTemp" in weather.columns:
            kpis["AverageTrackTemp"] = round(
                weather["TrackTemp"].mean(), 1
            )

        if "AirTemp" in weather.columns:
            kpis["AverageAirTemp"] = round(
                weather["AirTemp"].mean(), 1
            )

    return kpis

def get_winner(results: pd.DataFrame) -> pd.Series | None:

    if results.empty:
        return None

    winner = (
        results
        .sort_values("Position")
        .iloc[0]
    )

    return winner

def get_podium(results: pd.DataFrame) -> pd.DataFrame:

    if results.empty:
        return pd.DataFrame()

    return (
        results
        .sort_values("Position")
        .head(3)
        .reset_index(drop=True)
    )

def fastest_lap(laps: pd.DataFrame):

    if laps.empty:
        return None

    valid = laps.dropna(subset=["LapTime"])

    if valid.empty:
        return None

    return (
        valid
        .sort_values("LapTime")
        .iloc[0]
    )

def position_changes(results: pd.DataFrame) -> pd.DataFrame:

    if results.empty:
        return pd.DataFrame()

    df = results.copy()

    df["PositionsGained"] = (
        df["GridPosition"] - df["Position"]
    )

    return df[
        [
            "Abbreviation",
            "TeamName",
            "GridPosition",
            "Position",
            "PositionsGained",
            "Points",
        ]
    ].sort_values(
        "PositionsGained",
        ascending=False
    )


def average_race_pace(laps: pd.DataFrame) -> pd.DataFrame:

    if laps.empty:
        return pd.DataFrame()

    valid = laps.dropna(subset=["LapTime"])

    summary = (
        valid
        .groupby("Driver")
        .agg(
            AverageLap=("LapTime", "mean"),
            FastestLap=("LapTime", "min"),
            TotalLaps=("LapNumber", "count"),
        )
        .reset_index()
        .sort_values("AverageLap")
    )

    return summary

def team_summary(results: pd.DataFrame) -> pd.DataFrame:

    if results.empty:
        return pd.DataFrame()

    summary = (
        results
        .groupby("TeamName")
        .agg(
            Drivers=("DriverNumber", "count"),
            TotalPoints=("Points", "sum"),
            BestFinish=("Position", "min"),
        )
        .reset_index()
        .sort_values(
            "TotalPoints",
            ascending=False
        )
    )

    return summary


def driver_summary(results: pd.DataFrame,
                   driver: str):

    if results.empty:
        return None

    row = results[
        results["Abbreviation"] == driver
    ]

    if row.empty:
        return None

    return row.iloc[0]

def driver_consistency(laps: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates lap time consistency using
    the standard deviation of lap times.
    Lower value = More consistent.
    """

    if laps.empty:
        return pd.DataFrame()

    valid = laps.dropna(subset=["LapTime"]).copy()

    valid["LapTimeSeconds"] = valid["LapTime"].dt.total_seconds()

    summary = (
        valid
        .groupby("Driver")
        .agg(
            AverageLap=("LapTimeSeconds", "mean"),
            StdDeviation=("LapTimeSeconds", "std"),
            FastestLap=("LapTimeSeconds", "min"),
            TotalLaps=("LapNumber", "count")
        )
        .reset_index()
    )

    summary["ConsistencyScore"] = (
        100 - summary["StdDeviation"].fillna(0) * 8
    ).clip(lower=0)

    return summary.sort_values(
        "ConsistencyScore",
        ascending=False
    )

def tyre_usage(laps: pd.DataFrame) -> pd.DataFrame:

    if laps.empty:
        return pd.DataFrame()

    usage = (
        laps
        .groupby(["Driver", "Compound"])
        .size()
        .reset_index(name="Laps")
    )

    return usage.sort_values(
        ["Driver", "Laps"],
        ascending=[True, False]
    )

def stint_summary(laps: pd.DataFrame) -> pd.DataFrame:

    if laps.empty:
        return pd.DataFrame()

    summary = (
        laps
        .groupby(["Driver", "Stint", "Compound"])
        .agg(
            StartLap=("LapNumber", "min"),
            EndLap=("LapNumber", "max"),
            Laps=("LapNumber", "count")
        )
        .reset_index()
    )

    return summary

def speed_trap_summary(laps: pd.DataFrame) -> pd.DataFrame:

    if laps.empty:
        return pd.DataFrame()

    if "SpeedST" not in laps.columns:
        return pd.DataFrame()

    summary = (
        laps
        .groupby("Driver")
        .agg(
            MaxSpeed=("SpeedST", "max"),
            AvgSpeed=("SpeedST", "mean")
        )
        .reset_index()
        .sort_values(
            "MaxSpeed",
            ascending=False
        )
    )

    return summary

def weather_summary(weather: pd.DataFrame) -> dict:

    if weather.empty:
        return {}

    return {
        "Average Air Temp":
            round(weather["AirTemp"].mean(), 1),

        "Average Track Temp":
            round(weather["TrackTemp"].mean(), 1),

        "Humidity":
            round(weather["Humidity"].mean(), 1),

        "Average Wind":
            round(weather["WindSpeed"].mean(), 1),

        "Rain":
            bool(weather["Rainfall"].sum())
    }

def track_status_summary(track_status: pd.DataFrame) -> pd.DataFrame:

    if track_status.empty:
        return pd.DataFrame()

    summary = (
        track_status
        .groupby("Message")
        .size()
        .reset_index(name="Count")
        .sort_values(
            "Count",
            ascending=False
        )
    )

    return summary


def race_control_summary(messages: pd.DataFrame) -> pd.DataFrame:

    if messages.empty:
        return pd.DataFrame()

    summary = (
        messages
        .groupby("Category")
        .size()
        .reset_index(name="Messages")
        .sort_values(
            "Messages",
            ascending=False
        )
    )

    return summary


def position_progress(laps: pd.DataFrame,
                      driver: str) -> pd.DataFrame:

    if laps.empty:
        return pd.DataFrame()

    df = laps[
        laps["Driver"] == driver
    ][
        ["LapNumber", "Position"]
    ].copy()

    return df.sort_values("LapNumber")



def fastest_sectors(laps: pd.DataFrame) -> dict:

    if laps.empty:
        return {}

    valid = laps.dropna(
        subset=[
            "Sector1Time",
            "Sector2Time",
            "Sector3Time"
        ]
    )

    if valid.empty:
        return {}

    return {
        "Sector1":
            valid["Sector1Time"].min(),

        "Sector2":
            valid["Sector2Time"].min(),

        "Sector3":
            valid["Sector3Time"].min(),
    }

def compare_drivers(laps: pd.DataFrame,
                    driver1: str,
                    driver2: str) -> pd.DataFrame:
    """
    Compare two drivers.
    """

    if laps.empty:
        return pd.DataFrame()

    valid = laps.dropna(subset=["LapTime"]).copy()
    valid["LapTimeSeconds"] = valid["LapTime"].dt.total_seconds()

    drivers = valid[
        valid["Driver"].isin([driver1, driver2])
    ]

    summary = (
        drivers
        .groupby("Driver")
        .agg(
            AverageLap=("LapTimeSeconds", "mean"),
            FastestLap=("LapTimeSeconds", "min"),
            TotalLaps=("LapNumber", "count"),
            MaxSpeed=("SpeedST", "max")
        )
        .reset_index()
    )

    return summary



def compare_teams(results: pd.DataFrame) -> pd.DataFrame:

    if results.empty:
        return pd.DataFrame()

    summary = (
        results
        .groupby("TeamName")
        .agg(
            Drivers=("DriverNumber", "count"),
            TotalPoints=("Points", "sum"),
            BestFinish=("Position", "min")
        )
        .reset_index()
        .sort_values(
            "TotalPoints",
            ascending=False
        )
    )

    return summary


def performance_rating(position_gain: int,
                       consistency: float,
                       fastest_lap: bool):

    score = 50

    score += position_gain * 3

    score += consistency * 0.25

    if fastest_lap:
        score += 10

    return round(
        min(score, 100),
        1
    )



def generate_ai_insights(results: pd.DataFrame,
                         laps: pd.DataFrame,
                         weather: pd.DataFrame) -> list:

    insights = []

    if results.empty:
        return insights

    winner = get_winner(results)

    if winner is not None:
        insights.append(
            f"🏆 {winner['FullName']} won the race for {winner['TeamName']}."
        )

    gain = position_changes(results)

    if not gain.empty:

        best = gain.iloc[0]

        insights.append(
            f"📈 {best['Abbreviation']} gained "
            f"{best['PositionsGained']} positions."
        )

    fastest = fastest_lap(laps)

    if fastest is not None:

        insights.append(
            f"⚡ Fastest lap: "
            f"{fastest['Driver']} "
            f"in {fastest['LapTime']}."
        )

    weather_info = weather_summary(weather)

    if weather_info:

        insights.append(
            f"🌡 Average track temperature "
            f"{weather_info['Average Track Temp']}°C."
        )

    if len(insights) == 0:
        insights.append("No insights available.")

    return insights


def dashboard_cards(results,
                    laps,
                    weather):

    cards = calculate_session_kpis(
        results,
        laps,
        weather
    )

    return {
        "Drivers": cards["Drivers"],
        "Finishers": cards["Finishers"],
        "Race Laps": cards["TotalLaps"],
        "Track Temp": cards["AverageTrackTemp"]
    }

def format_laptime(value):

    if pd.isna(value):
        return "-"

    try:
        minutes = int(value.total_seconds() // 60)
        seconds = value.total_seconds() % 60

        return f"{minutes}:{seconds:06.3f}"

    except Exception:
        return str(value)

__all__ = [
    "calculate_session_kpis",
    "get_winner",
    "get_podium",
    "fastest_lap",
    "position_changes",
    "average_race_pace",
    "team_summary",
    "driver_summary",
    "driver_consistency",
    "tyre_usage",
    "stint_summary",
    "speed_trap_summary",
    "weather_summary",
    "track_status_summary",
    "race_control_summary",
    "position_progress",
    "fastest_sectors",
    "compare_drivers",
    "compare_teams",
    "performance_rating",
    "generate_ai_insights",
    "dashboard_cards",
    "format_laptime",

    "biggest_gainer",
    "biggest_loser",
    "pole_sitter",
]


def biggest_gainer(results):

    data = results.copy()

    data["Change"] = (
        data["GridPosition"] -
        data["Position"]
    )

    return data.sort_values(
        "Change",
        ascending=False
    ).iloc[0]


def biggest_loser(results):

    data = results.copy()

    data["Change"] = (
        data["GridPosition"] -
        data["Position"]
    )

    return data.sort_values(
        "Change"
    ).iloc[0]


def pole_sitter(results):

    return results.loc[
        results["GridPosition"] == 1
    ].iloc[0]