from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
from beautiful_date import Jan, Apr
import os
from dotenv import load_dotenv
from retrieve_games import get_games_portugal

load_dotenv()
email_address = os.getenv("email_address")

calendar = GoogleCalendar(
    email_address, credentials_path=".credentials/credentials.json"
)


def create_event():
    event = Event(
        "Test 2",
        start=(1 / Apr / 2025)[9:00],
        minutes_before_email_reminder=50,
    )
    return event


def main():
    list = get_games_portugal()

    for match in list:
        print(match["homeTeam"])
        print(match["awayTeam"])
        print(match["competition"])
        print(match["broadcastOperator"])
        print(match["matchDate"])
    # event = create_event()
    # calendar.add_event(event)

    # for event in calendar:
    #     print(event)


if __name__ == "__main__":
    main()
