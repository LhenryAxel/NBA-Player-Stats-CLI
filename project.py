import sys
from typing import Any, Dict, List, Optional

import requests

# Base URL of the NBA API
API_BASE = "https://api.balldontlie.io/v1"

# API key required to access the NBA API
API_KEY = "4764f25d-c0c9-4217-af4c-31522dd30d9d"


def main() -> None:
    """
    Main entry point of the program.
    - Reads the player name from command-line arguments
    - Fetches player data from the API
    - Displays formatted player information
    """
    if len(sys.argv) != 2:
        sys.exit('Usage: python project.py "Player Name"')

    # Normalize user input
    query = normalize_player_name(sys.argv[1])
    if not query:
        sys.exit("Error: Empty player name.")

    # Call the API to fetch players
    try:
        players = fetch_player_data(query)
    except requests.RequestException:
        sys.exit("Error: NBA API unreachable.")

    # Select the best matching player
    player = validate_player_result(players, query)
    if player is None:
        sys.exit("Error: Player not found.")

    # Display the player information
    print(format_player_info(player))


def normalize_player_name(name: str) -> str:
    """
    Cleans and normalizes the player name entered by the user.
    - Removes extra spaces
    - Converts to lowercase
    """
    return " ".join(name.strip().lower().split())


def fetch_player_data(query: str) -> List[Dict[str, Any]]:
    """
    Sends a request to the NBA API to search for players.
    Returns a list of players matching the query.
    """
    url = f"{API_BASE}/players"
    params = {"search": query}
    headers = {"Authorization": API_KEY}

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()["data"]


def validate_player_result(
    players: List[Dict[str, Any]],
    normalized_query: str
) -> Optional[Dict[str, Any]]:
    """
    Selects the most relevant player from the API results.
    - Returns None if no player is found
    - Returns the exact match if possible
    - Otherwise returns the first result
    """
    if not players:
        return None

    if len(players) == 1:
        return players[0]

    for player in players:
        full_name = normalize_player_name(
            player["first_name"] + " " + player["last_name"]
        )
        if full_name == normalized_query:
            return player

    return players[0]


def format_player_info(player: Dict[str, Any]) -> str:
    """
    Formats the player data into a readable string.
    Handles missing fields by displaying 'N/A'.
    """
    team = player.get("team", {}).get("full_name") or "N/A"

    height = player.get("height") or "N/A"
    weight_value = player.get("weight")
    weight = f"{weight_value} lbs" if weight_value else "N/A"

    position = player.get("position") or "N/A"
    full_name = (
        player.get("first_name", "") + " " + player.get("last_name", "")
    ).strip() or "Unknown"

    return (
        "Player: " + full_name + "\n"
        "Team: " + team + "\n"
        "Position: " + position + "\n"
        "Height: " + height + "\n"
        "Weight: " + weight
    )


if __name__ == "__main__":
    main()