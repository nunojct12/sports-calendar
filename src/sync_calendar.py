from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
import os
from dotenv import load_dotenv
from retrieve_games import get_football_events
from datetime import datetime, timedelta


load_dotenv()
email_address = os.getenv("email_address")
calendar_id = os.getenv("calendar_id")

calendar = GoogleCalendar(
    email_address, credentials_path=".credentials/credentials.json"
)


def create_event(title: str, description: str, match_date: datetime):
    event = Event(
        title,
        description=description,
        start=match_date,
        end=match_date + timedelta(hours=2),
        default_reminders=True,
    )

    calendar.add_event(
        event,
        calendar_id=calendar_id,
    )


def update_event_time(previous_event: Event, match_date: datetime):
    previous_event.start = match_date
    previous_event.end = match_date + timedelta(hours=2)
    calendar.update_event(previous_event, calendar_id=calendar_id)


def get_calendar_events():
    calendar_events_list = calendar.get_events(
        time_min=datetime.now(), calendar_id=calendar_id
    )
    previous_events_dict = {}
    for event in calendar_events_list:
        previous_events_dict[event.summary] = event

    return previous_events_dict


def add_events_to_calendar(matches_list: list):
    calendar_events = get_calendar_events()

    for match in matches_list:
        title = f'{match["homeTeam"]} vs {match["awayTeam"]}'
        description = f'Competition: {match["competition"]}'
        match_date = match["matchDate"]

        existing_match_event = (
            calendar_events[title] if title in calendar_events else False
        )

        if not existing_match_event:  # if event doesn't exist, create it
            print(title, description, match_date)
            create_event(title, description, match_date)
        else:
            if (
                existing_match_event.start.timestamp() != match_date.timestamp()
            ):  # if event exists, but has a different start time (due to the match time being updated), update the event
                update_event_time(existing_match_event, match_date)


def main():
    matches_list = get_football_events()

    add_events_to_calendar(matches_list)


if __name__ == "__main__":
    main()
