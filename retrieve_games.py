import datetime
from datetime import timedelta
import requests
from zoneinfo import ZoneInfo

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
    # url = f"https://www.ligaportugal.pt/api/v1/team/matches?id={fcporto_id}&season=20242025&filter=next&limit=true"
    url = "https://www.sofascore.com/api/v1/team/3002/events/next/0"

    response = requests.get(url).json()
    matches = safe_get(response, "events")
    matches_dict = []

    for match in matches:
        new_match = {}
        if safe_get(match, "detailId") == 1:
            new_match["homeTeam"] = safe_get(match, "homeTeam", "name")
            new_match["awayTeam"] = safe_get(match, "awayTeam", "name")
            new_match["competition"] = safe_get(match, "tournament", "name")
            new_match["matchDate"] = datetime.datetime.fromtimestamp(
                safe_get(match, "startTimestamp")
            )

            matches_dict.append(new_match)

    return matches_dict


def main():
    get_games_portugal()


if __name__ == "__main__":
    main()
