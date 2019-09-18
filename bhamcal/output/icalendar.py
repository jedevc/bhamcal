from uuid import uuid4 as uuid

def iCalendar(events):
    ical = '\r\n'.join([
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//University of Birmingham//Web timetables//EN'
    ])

    for event in events:
        vevent = [
            "BEGIN:VEVENT",
            "UID:" + str(uuid()),
            "SUMMARY:" + event.subject,
            "DTSTAMP:" + format_date(event.start),
            "DTSTART:" + format_date(event.start),
            "DTEND:" + format_date(event.end),
            "DESCRIPTION:" + event.description.replace('\n', r'\n'),
            "LOCATION:" + event.location,
            "END:VEVENT"
        ]
        vevent = '\r\n'.join(vevent)
        ical += '\r\n' + vevent

    ical += '\r\nEND:VCALENDAR'

    return ical

def format_date(date):
    return date.strftime("%Y%m%dT%H%M%S")