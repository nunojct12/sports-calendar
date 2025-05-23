from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
import os
from dotenv import load_dotenv
from retrieve_games import get_formula1_events, get_football_events
from datetime import datetime, timedelta
import argparse


load_dotenv()
email_address = os.getenv("email_address")
calendar_id = os.getenv("calendar_id")

calendar = GoogleCalendar(
    email_address, credentials_path=".credentials/credentials.json"
)


def create_event(
    title: str, description: str, match_date: datetime, match_end_date: datetime
):
    event = Event(
        title,
        description=description,
        start=match_date,
        end=match_end_date,
        default_reminders=True,
    )

    calendar.add_event(
        event,
        calendar_id=calendar_id,
    )


def update_event_time(
    previous_event: Event, match_date: datetime, match_end_date: datetime
):
    previous_event.start = match_date
    previous_event.end = match_end_date
    calendar.update_event(previous_event, calendar_id=calendar_id)


def get_calendar_events():
    calendar_events_list = calendar.get_events(
        time_min=datetime.now(), calendar_id=calendar_id
    )
    previous_events_dict = {}
    for event in calendar_events_list:
        previous_event_title = f"{event.summary} - {event.description}"
        previous_events_dict[previous_event_title] = event

    return previous_events_dict


def add_football_matches_to_calendar(matches_list: list):
    calendar_events = get_calendar_events()

    for match in matches_list:
        title = f'{match["homeTeam"]} vs {match["awayTeam"]}'
        description = f'Competition: {match["competition"]}\nRound: {match["round"]}'
        match_date = match["matchDate"]
        match_end_date = match_date + timedelta(hours=2)

        search_previous_event_title = f"{title} - {description}"
        existing_match_event = (
            calendar_events[search_previous_event_title]
            if search_previous_event_title in calendar_events
            else False
        )

        if not existing_match_event:  # if event doesn't exist, create it
            print(f"Adding a new event: {title}")
            create_event(title, description, match_date, match_end_date)
        else:
            if (
                existing_match_event.start.timestamp() != match_date.timestamp()
            ):  # if event exists, but has a different start time (due to the match time being updated), update the event
                print(f"Updating an event: {title}")
                update_event_time(existing_match_event, match_date, match_end_date)


def add_f1_events_to_calendar(f1_events_list: list):
    calendar_events = get_calendar_events()

    for event in f1_events_list:
        title = f'{event["gp"]} - {event["stageName"]}'
        description = f'Circuit: {event["circuit"]} - {event["circuitCity"]}, {event["circuitCountry"]}'
        event_date = event["startDate"]
        event_end_date = event_date + timedelta(hours=1)
        if event["stageName"] == "Race":
            event_end_date = event_date + timedelta(hours=2)

        search_previous_event_title = f"{title} - {description}"
        existing_f1_event = (
            calendar_events[search_previous_event_title]
            if search_previous_event_title in calendar_events
            else False
        )

        if not existing_f1_event:  # if event doesn't exist, create it
            print(f"Adding a new event: {title}")
            create_event(title, description, event_date, event_end_date)
        else:
            if (
                existing_f1_event.start.timestamp() != event_date.timestamp()
            ):  # if event exists, but has a different start time (due to the match time being updated), update the event
                print(f"Updating an event: {title}")
                update_event_time(existing_f1_event, event_date, event_end_date)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--f1-events",
    action=argparse.BooleanOptionalAction,
    help="Enable or disable adding Formula 1 events to the calendar.",
    default=True,
)
parser.add_argument(
    "--football-events",
    action=argparse.BooleanOptionalAction,
    help="Enable or disable adding Football events to the calendar.",
    default=True,
)
args = parser.parse_args()
f1_events = args.f1_events
football_events = args.football_events


def main():
    if football_events:
        football_matches_list = get_football_events()
        add_football_matches_to_calendar(football_matches_list)

    if f1_events:
        formula1_events = get_formula1_events()
        add_f1_events_to_calendar(formula1_events)


if __name__ == "__main__":
    main()
