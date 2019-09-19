import re
from datetime import datetime

from bs4 import BeautifulSoup

from .event import CalendarEvent

def extract(frame):
    soup = BeautifulSoup(frame, 'html.parser')
    spreadsheets = soup.find_all('table', class_='spreadsheet')

    for spreadsheet in spreadsheets:
        rows = spreadsheet.find_all('tr')[1:]
        for row in rows:
            yield extract_event(row)

def extract_event(table_row):
    entries = table_row.find_all('td')
    entries = [entry.string.strip() for entry in entries]

    # extract data from table
    day = entries[0]
    title = entries[1]
    event_type = entries[2]
    start_time = entries[3]
    end_time = entries[4]
    location = entries[5]
    lecturer = entries[6]
    department = entries[7]

    # process subject title
    name = title.split('/')[0]
    name = re.sub(r"\([^)]*\)", "", name)
    name = name.strip()

    # build description
    description = ""
    description += 'With: ' + lecturer + '\n'
    description += 'Activity: ' + title + '\n'
    description += 'Type: ' + event_type + '\n'
    description += 'Department: ' + department

    return CalendarEvent(
        start=extract_datetime(day, start_time),
        end=extract_datetime(day, end_time),
        subject=name,
        location=location,
        description=description
    )

def extract_datetime(date, time):
    return datetime.strptime(date + " " + time, "%d %b %Y %H:%M")
