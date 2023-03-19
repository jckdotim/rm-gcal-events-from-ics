import os
import datetime
import argparse
import pickle
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from icalendar import Calendar, Event
from dateutil.parser import parse

def main(args):
    # Read and parse the .ics file
    with open(args.input, 'r') as file:
        calendar = Calendar.from_ical(file.read())

    # Collect the events from the parsed .ics file
    events_to_remove = []
    for component in calendar.walk():
        if component.name == 'VEVENT':
            events_to_remove.append(component)

    # Google Calendar API setup
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Get the primary calendar
    calendar_id = 'primary'

    # Iterate through the events to remove and delete them from the primary Google Calendar
    for event in events_to_remove:
        start_time = event['DTSTART'].dt
        end_time = event['DTEND'].dt

        # Convert date-time objects to RFC3339 format
        start_time_rfc3339 = parse(start_time.isoformat()).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        end_time_rfc3339 = parse(end_time.isoformat()).strftime('%Y-%m-%dT%H:%M:%S.%f%z')

        # Search for events that match the start and end times of the .ics events
        events_result = service.events().list(calendarId=calendar_id, timeMin=start_time_rfc3339,
                                              timeMax=end_time_rfc3339, singleEvents=True,
                                              orderBy='startTime').execute()
        matching_events = events_result.get('items', [])

        # Delete the matching events
        for matching_event in matching_events:
            service.events().delete(calendarId=calendar_id, eventId=matching_event['id']).execute()
            print(f"Deleted event '{matching_event['summary']}' with ID '{matching_event['id']}'")

    print('All events from the .ics file have been removed from the Google Calendar.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove all Google Calendar events created by a specific .ics file.')
    parser.add_argument('input', metavar='INPUT', type=str, help='Path to the input .ics file.')

    args = parser.parse_args()
    main(args)
