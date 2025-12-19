import sys
from typing import Any, Dict, List, Optional

import requests


API_BASE = "https://www.balldontlie.io/api/v1"


def main() -> None:
    """
    CLI usage:
        python project.py "LeBron James"
    """
    if len(sys.argv) != 2:
        sys.exit('Usage: python project.py "Player Name"')

    raw_name = sys.argv[1]
    name = normalize_player_name(raw_name)

    if not name:
        sys.exit("Error: Please provide a non-empty player name.")

    try:
        players = fetch_player_data(name)
    except requests.RequestException:
        sys.exit("Error: NBA API is unreachable right now. Please try again later.")

    player = validate_player_result(players, name)
    if player is None:
        sys.exit("Error: No matching player found.")

    print(format_player_info(player))


def normalize_player_name(name: str) -> str:
    """
    Normalize user input:
    - trim leading/trailing spaces
    - collapse multiple spaces
    - lowercase for consistent searching
    """
    if not isinstance(name, str):
        return ""
    parts = name.strip().split()
    return " ".join(parts).lower()


def fetch_player_data(name: str) -> List[Dict[str, Any]]:
    """
    Fetch players from balldontlie matching the search string.
    Returns a list of player dicts.
    Raises requests.RequestException on network / HTTP errors.
    """
    url = f"{API_BASE}/players"
    params = {"search": name, "per_page": 100}

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # balldontlie format: {"data": [...], "meta": {...}}
    players = data.get("data", [])
    if not isinstance(players, list):
        return []
    return players


def validate_player_result(players: List[Dict[str, Any]], normalized_query: str) -> Optional[Dict[str, Any]]:
    """
    Decide which player to return.
    - If no players -> None
    - If one player -> that player
    - If multiple players -> prefer an exact full-name match (case-insensitive),
      otherwise return the first result.
    """
    if not players:
        return None

    if len(players) == 1:
        return players[0]

    # Prefer exact match on "first_name last_name"
    for p in players:
        full = normalize_player_name(f"{p.get('first_name', '')} {p.get('last_name', '')}")
        if full == normalized_query:
            return p

    # Otherwise, best-effort: first result
    return players[0]


def format_player_info(player: Dict[str, Any]) -> str:
    """
    Convert player JSON dict into a readable multiline string.
    Handles missing fields gracefully.
    """
    first = player.get("first_name", "")
    last = player.get("last_name", "")
    position = player.get("position") or "N/A"

    team = player.get("team") or {}
    team_city = team.get("city", "")
    team_name = team.get("name", "")
    team_full = " ".join(part for part in [team_city, team_name] if part).strip() or "N/A"

    height_feet = player.get("height_feet")
    height_inches = player.get("height_inches")
    if height_feet is None or height_inches is None:
        height = "N/A"
    else:
        height = f"{height_feet}-{height_inches}"

    weight_pounds = player.get("weight_pounds")
    weight = f"{weight_pounds} lbs" if isinstance(weight_pounds, int) else "N/A"

    full_name = " ".join(part for part in [first, last] if part).strip() or "Unknown"

    return (
        f"Player: {full_name}\n"
        f"Team: {team_full}\n"
        f"Position: {position}\n"
        f"Height: {height}\n"
        f"Weight: {weight}"
    )


if __name__ == "__main__":
    main()
