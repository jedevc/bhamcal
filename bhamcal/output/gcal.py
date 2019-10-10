import pickle
import time
import datetime

from collections import Counter

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
TIME_DELTA = 0.2

def googleCalendar(calendar, events):
    # try to access credentials
    creds = None
    try:
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    except FileNotFoundError:
        pass

    # without valid credentials, try to login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    codes = Counter()

    for event in events:
        codes[event.uid] += 1

        body = {
            'summary': event.subject,
            'location': event.location,
            'description': event.description,
            'start': {
                'dateTime': event.start.isoformat() 
            },
            'end': {
                'dateTime': event.end.isoformat()
            },
            'iCalUID': event.uid + str(codes[event.uid])
        }

        service.events().import_(calendarId=calendar, body=body).execute()

        # avoid getting rate-limited
        # TODO: only run this when you actually get rate-limited
        time.sleep(TIME_DELTA)
