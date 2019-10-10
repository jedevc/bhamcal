from collections import Counter

def iCalendar(filename, events):
    codes = Counter()

    with open(filename, 'w') as output:
        header = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//University of Birmingham//Web timetables//EN'
        ]
        output.write('\r\n'.join(header) + '\r\n')

        for event in events:
            codes[event.uid] += 1

            vevent = [
                "BEGIN:VEVENT",
                "UID:" + event.uid + str(codes[event.uid]),
                "SUMMARY:" + event.subject,
                "DTSTAMP:" + format_date(event.start),
                "DTSTART:" + format_date(event.start),
                "DTEND:" + format_date(event.end),
                "DESCRIPTION:" + event.description.replace('\n', r'\n'),
                "LOCATION:" + event.location,
                "END:VEVENT"
            ]
            output.write('\r\n'.join(vevent) + '\r\n')

        output.write('END:VCALENDAR')

def format_date(date):
    return date.strftime("%Y%m%dT%H%M%SZ")
