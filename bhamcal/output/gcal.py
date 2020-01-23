import pickle
import time
import datetime

from collections import Counter

from ..utils import log
from ..utils import Message

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
TIME_DELTA = 0.2

def googleCalendar(calendar, events, use_colors=False):
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
    batch = service.new_batch_http_request()
    codes = Counter()
    counter = 0
    if use_colors:
        available_colors = list(service.colors().get().execute()['event'].keys())
        selector = ColorSelector(available_colors)
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
            # NOTE: sequence "guarantees" that each calendar contains the
            #       most recent events, just like for the iCalendar export
            'sequence': int(time.time()),
            'iCalUID': event.uid + str(codes[event.uid])
        }
        if use_colors:
            body['colorId'] = selector[event.subject_code]
        batch.add(service.events().import_(calendarId=calendar, body=body))
        counter += 1
        log(f'{counter}/{len(events)} events processed',Message.INFO, overwrite=(counter != len(events)))
    log(f'uploading {len(events)} to gcal', Message.INFO)
    batch.execute()

class ColorSelector:
    def __init__(self, colors):
        half = len(colors) // 2
        self.original = []
        for i in range(half):
            self.original.extend(colors[i::half])

        self.colors = self.original

        self.cache = {}

    def __getitem__(self, index):
        if index in self.cache:
            return self.cache[index]
        else:
            try:
                color = self.colors.pop(0)
            except IndexError:
                self.colors = self.original
                color = self.colors.pop(0)

            self.cache[index] = color
            return color
