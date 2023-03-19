# Remove Google Calendar Events

This script, `remove_gcal_events.py`, is a command-line tool that removes all events from your primary Google Calendar that were created by a specific .ics file.

## Prerequisites

Before you begin, you'll need to have the following:

1. Python 3 installed on your machine.
2. The Google Calendar API enabled and a `client_secret.json` file obtained by following the [Python Quickstart guide](https://developers.google.com/calendar/quickstart/python).
3. The following Python packages installed:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib icalendar
```

## Usage

1. Save the `remove_gcal_events.py` script to your local machine.

2. Open a terminal or command prompt and navigate to the folder where you saved the script.

3. Run the script with the following command:

```bash
python remove_gcal_events.py path/to/yourfile.ics
```

Replace `path/to/yourfile.ics` with the path to the .ics file containing the events you want to remove from your primary Google Calendar.

4. If this is the first time you're running the script, a new browser window will open asking you to authorize the script to access your Google Calendar. Grant the necessary permissions, and the script will remove the matching events from your calendar.
