
# sports-calendar

  

Add favorite teams and sports events to Google calendar

  

## How to use
### Setup

1.  Create a virtual env  `python3 -m venv .venv`
2.  Activate the virtual env  `source .venv/bin/activate`
3.  Run  `pip install -r requirements.txt`

To access your Google Calendar, the project uses the [Google Calendar Simple API (gcsa)](https://github.com/kuzmoyev/google-calendar-simple-api). Setup the gcsa credentials by following the [gcsa setup documentation](https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html#credentials)
After you´ve created your Google Cloud Platform (GCP) project, and get the `credentials.json`, on the first run, an authentication screen will be displayed, and you should login with your google account. After that, on the same `.credentials` folder, a new file `token.pickle` will be created - this will be your token, so you don´t have to login every time. This token is valid for 7 days, if you want an unlimited token, you must deploy your GCP project to production.


Go to https://www.sofascore.com/ and search for a football team. From the url, get the team id and add it to the `team_ids.json` file that is on the `data` folder.

Create a .env file on the root folder and add the following:

    email_address="example@gmail.com"
    calendar_id="123456789@group.calendar.google.com"
Add the `calendar_id` only if you want to add the events to a specific calendar. If you want to add them to the primary calendar, you don´t have to add this field, and the primary calendar will be used as default. In my case, I created a Sports calendar on my Google Calendar account, so that I can easily show/hide these events.


### Run script

From the root folder

-   `python3 src/sync_calendar.py` 
-   `--no-football-events`  - Doesn´t add football events
-   `--no-f1-events`  - Doesn´t add Formula1 events