from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
from beautiful_date import Jan, Apr
import os
from dotenv import load_dotenv
from retrieve_games import get_games_portugal
from datetime import datetime, timedelta
from dateutil import tz

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
    return event


def main():
    list = get_games_portugal()

    for match in list:
        pt_time = tz.gettz("Europe / Lisbon")
        match_date = datetime.strptime(
            match["matchDate"], "%Y-%m-%dT%H:%M:%SZ"
        ).astimezone(tz=pt_time)

        title = f'{match["homeTeam"]} vs {match["awayTeam"]}'
        description = f'Competition: {match["competitionName"]}\nBroadcaster: {match["broadcastOperator"]}'

        print(title)
        print(description)
        print(match_date)
        new_event = create_event(title, description, match_date)
        calendar.add_event(
            new_event,
            calendar_id=calendar_id,
        )
        return


if __name__ == "__main__":
    main()
