from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
from beautiful_date import Jan, Apr
import os
from dotenv import load_dotenv
import requests

load_dotenv()
email_address = os.getenv("email_address")
api_key = os.getenv("api_key")

calendar = GoogleCalendar(
    email_address, credentials_path=".credentials/credentials.json"
)


def create_event():
    event = Event(
        "Test 2",
        start=(1 / Apr / 2025)[9:00],
        # recurrence=[
        #     Recurrence.rule(freq=DAILY),
        #     Recurrence.exclude_rule(by_week_day=[SU, SA]),
        #     Recurrence.exclude_times([
        #         (19 / Apr / 2019)[9:00],
        #         (22 / Apr / 2019)[9:00]
        #     ])
        # ],
        minutes_before_email_reminder=50,
    )
    return event


def main():
    url = "https://www.thesportsdb.com/api/v1/json/3/eventsnext.php?id=134114"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    # event = create_event()
    # calendar.add_event(event)

    # for event in calendar:
    #     print(event)


if __name__ == "__main__":
    main()
