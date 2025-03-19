import requests

fcporto_id = 157
felgueiras_id = 142


def safe_get(data, *keys, default="Unknown"):
    """Safely get a nested value from a dictionary."""
    try:
        for key in keys:
            data = data.get(key, {})
        return data if data else default
    except:
        return default


def get_games_portugal():
    url = f"https://www.ligaportugal.pt/api/v1/team/matches?id={fcporto_id}&season=20242025&filter=next&limit=true"

    matches = requests.get(url).json()

    matches_dict = []

    for match in matches:
        new_match = {}
        if safe_get(match, "fixtureDateIsDefined") == True:
            new_match["homeTeam"] = safe_get(match, "homeTeam", "name")
            new_match["awayTeam"] = safe_get(match, "awayTeam", "name")
            new_match["competition"] = safe_get(match, "competitionName")
            new_match["broadcastOperator"] = safe_get(match, "broadcastOperator")
            new_match["matchDate"] = safe_get(match, "matchDate")

            matches_dict.append(new_match)

    return matches_dict
