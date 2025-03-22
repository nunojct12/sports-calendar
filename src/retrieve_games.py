import datetime
import json
import cloudscraper


def safe_get(data, *keys, default="Unknown"):
    """Safely get a nested value from a dictionary."""
    try:
        for key in keys:
            data = data.get(key, {})
        return data if data else default
    except:
        return default


def get_team_ids():
    try:
        with open("data/team_ids.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def get_football_events():
    team_to_retrieve = get_team_ids()
    matches_dict = []

    for team, team_id in team_to_retrieve.items():
        url = f"https://www.sofascore.com/api/v1/team/{team_id}/events/next/0"

        scraper = cloudscraper.create_scraper()
        scraped_text = scraper.get(url).text
        response = json.loads(scraped_text)

        matches = safe_get(response, "events")

        for match in matches:
            new_match = {}
            if safe_get(match, "detailId") != "Unknown":
                new_match["homeTeam"] = safe_get(match, "homeTeam", "name")
                new_match["awayTeam"] = safe_get(match, "awayTeam", "name")
                new_match["competition"] = safe_get(match, "tournament", "name")
                new_match["matchDate"] = datetime.datetime.fromtimestamp(
                    safe_get(match, "startTimestamp")
                )

                matches_dict.append(new_match)

    return matches_dict


def main():
    get_football_events()


if __name__ == "__main__":
    main()
