from project import (
    normalize_player_name,
    validate_player_result,
    format_player_info,
)


def test_normalize_player_name_basic():
    assert normalize_player_name("LeBron James") == "lebron james"


def test_normalize_player_name_whitespace():
    assert normalize_player_name("  Stephen   Curry  ") == "stephen curry"


def test_normalize_player_name_uppercase():
    assert normalize_player_name("KEVIN DURANT") == "kevin durant"


def test_validate_player_result_none():
    assert validate_player_result([], "lebron james") is None


def test_validate_player_result_single():
    players = [
        {"first_name": "LeBron", "last_name": "James"}
    ]
    result = validate_player_result(players, "lebron james")
    assert result == players[0]


def test_validate_player_result_exact_match_preferred():
    players = [
        {"first_name": "LeBron", "last_name": "James"},
        {"first_name": "LeBron", "last_name": "Johnson"},
    ]
    result = validate_player_result(players, "lebron james")
    assert result["last_name"] == "James"


def test_format_player_info_complete():
    player = {
        "first_name": "Stephen",
        "last_name": "Curry",
        "position": "G",
        "height": "6-2",
        "weight": "185",
        "team": {
            "full_name": "Golden State Warriors",
        },
    }

    output = format_player_info(player)

    assert "Stephen Curry" in output
    assert "Golden State Warriors" in output
    assert "Position: G" in output
    assert "Height: 6-2" in output
    assert "185 lbs" in output


def test_format_player_info_missing_fields():
    player = {
        "first_name": "Test",
        "last_name": "Player",
        "position": None,
        "height": None,
        "weight": None,
        "team": {
            "full_name": None,
        },
    }

    output = format_player_info(player)

    assert "Test Player" in output
    assert "Team: N/A" in output
    assert "Position: N/A" in output
    assert "Height: N/A" in output
    assert "Weight: N/A" in output
