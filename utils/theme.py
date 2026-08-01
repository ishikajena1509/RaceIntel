"""
=========================================================
RaceIntel Theme
=========================================================
"""

TEAM_COLORS = {
    "Mercedes": "#00D2BE",
    "Ferrari": "#DC0000",
    "McLaren": "#FF8700",
    "Red Bull Racing": "#3671C6",
    "Williams": "#005AFF",
    "Aston Martin": "#006F62",
    "Alpine": "#0090FF",
    "Haas F1 Team": "#B6BABD",
    "Racing Bulls": "#6692FF",
    "Kick Sauber": "#52E252",
}


def get_team_color(team_name: str) -> str:
    """
    Returns the official team color.
    """

    return TEAM_COLORS.get(team_name, "#E10600")