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


def get_football_team_ids():
    try:
        with open("data/team_ids.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def get_football_events():
    team_to_retrieve = get_football_team_ids()
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


def get_formula1_events():
    gps_dict = []
    gp_events_list = [
        "Practice 1",
        "Practice 2",
        "Practice 3",
        "Qualification 1",
        "Race",
        "Sprint Shootout 1",
        "Sprint",
    ]

    url = "https://www.sofascore.com/api/v1/stage/209766/substages"

    scraper = cloudscraper.create_scraper()
    scraped_text = scraper.get(url).text
    response = json.loads(scraped_text)

    grand_prixs = safe_get(response, "stages")

    for gp in grand_prixs:

        if safe_get(gp, "status", "type") == "notstarted":
            gp_substages = safe_get(gp, "eventSubstages")
            for gp_substage in gp_substages:
                if safe_get(gp_substage, "name") in gp_events_list:
                    new_gp = {}
                    stage_name = safe_get(gp_substage, "name")
                    if stage_name == "Qualification 1":
                        new_gp["stageName"] = "Qualification"
                    elif stage_name == "Sprint Shootout 1":
                        new_gp["stageName"] = "Sprint Shootout"
                    else:
                        new_gp["stageName"] = stage_name
                    new_gp["gp"] = safe_get(gp_substage, "stageParent", "description")
                    new_gp["startDate"] = datetime.datetime.fromtimestamp(
                        safe_get(gp_substage, "startDateTimestamp")
                    )
                    new_gp["circuit"] = safe_get(gp, "info", "circuit")
                    new_gp["circuitCity"] = safe_get(gp, "info", "circuitCity")
                    new_gp["circuitCountry"] = safe_get(gp, "info", "circuitCountry")

                    gps_dict.append(new_gp)

    return gps_dict
