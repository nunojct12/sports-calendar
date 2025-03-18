import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_events(creds):
    service = build("calendar", "v3", credentials=creds)

  # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

def create_event(creds):
  service = build("calendar", "v3", credentials=creds)

  event = {
    "summary" : "Jogo do porto",
    "location" : "Estádio do Dragoum",
    "description" : "Isto é um jogo de futebol",
    "colorId" : 5,
    "start": {
      "dateTime" : "2024-01-29T22:00:00+01:00",
      "timeZone" : "Europe/Berlin",
    },
     "end": {
      "dateTime" : "2024-01-29T23:00:00+01:00",
      "timeZone" : "Europe/Berlin",
    }
  }

  event = service.events().insert(calendarId="primary", body=event).execute()

  print(f"Event created {event.get('htmlLink')}")

  

def manage_events(): 
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json")
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    get_events(creds)

  except HttpError as error:
    print(f"An error occurred: {error}")


