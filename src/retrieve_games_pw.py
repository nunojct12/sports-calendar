import re
from playwright.sync_api import Page, Playwright, sync_playwright
import datetime


def get_football_events():
    with sync_playwright() as playwright:
        chromium = playwright.chromium
        browser = chromium.launch()
        page = browser.new_page()

        matches_dict = []
        page.goto("https://www.flashscore.com/team/fc-porto/S2NmScGp/fixtures/")
        elements = page.query_selector_all(".event__match")
        matches_url_list = []
        for element in elements:
            if element.query_selector("a.event__icon"):
                a_tag = element.query_selector("a")
                href = a_tag.get_attribute("href")
                matches_url_list.append(href)

        for match_url in matches_url_list:
            page.goto(match_url)

            start_time = page.query_selector(".duelParticipant__startTime").inner_text()
            competition_elements = page.query_selector_all(".wcl-breadcrumbItem_CiWQ7")

            start_time = datetime.datetime.strptime(
                start_time, "%d.%m.%Y %H:%M"
            ).astimezone(datetime.timezone(datetime.timedelta(hours=2)))

            new_match = {}

            new_match["homeTeam"] = page.query_selector(
                ".duelParticipant__home"
            ).inner_text()
            new_match["awayTeam"] = page.query_selector(
                ".duelParticipant__away"
            ).inner_text()
            new_match["competition"] = competition_elements[2].text_content()
            new_match["matchDate"] = start_time

            matches_dict.append(new_match)
            break

        print("Matches Dictionary:")
        for match in matches_dict:
            print(match)

        return matches_dict


if __name__ == "__main__":
    get_football_events()
