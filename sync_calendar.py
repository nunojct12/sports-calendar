from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
from beautiful_date import Jan, Apr
import os
from dotenv import load_dotenv
from retrieve_games import get_games_portugal
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
        timezone="UTC",
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


def main():
    calendar_events_list = calendar.get_events(
        time_min=datetime.now(), calendar_id=calendar_id, timezone="UTC"
    )
    previous_events_dict = {}
    for event in calendar_events_list:
        previous_events_dict[event.summary] = event

    match_list = get_games_portugal()

    for match in match_list:
        title = f'{match["homeTeam"]} vs {match["awayTeam"]}'
        description = f'Competition: {match["competitionName"]}\nBroadcaster: {match["broadcastOperator"]}'
        match_date = match["matchDate"]
        previous_event = (
            previous_events_dict[title] if len(previous_events_dict) > 0 else False
        )

        if not previous_event:  # if event doesn't exist, create it
            create_event(title, description, match_date)
        else:
            if (
                previous_event.start
                != match_date  # FIXME: date returned is not in the correct timezone. Need to figure out why
            ):  # end=match_date + timedelta(hours=2), if event exists, but has a different start time (due to the match time being updated), update the event
                update_event_time(previous_event, match_date)

        return


if __name__ == "__main__":
    main()
