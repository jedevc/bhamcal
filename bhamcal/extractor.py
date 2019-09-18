from .event import CalendarEvent
from datetime import datetime

def cutSectionFromText(text, start, end):
    return text[:start] + text[end:]

def getTableFromFrame(text):
    text = text.replace('\n', '').replace('\r', '')

    # cuts off top
    startPosition = text.find("""<p><span class="labelone">""") - len("</table>")
    text = text[startPosition:]
    # cuts off bottom
    endPosition = text.find("""<table class="footer-border-args" """)
    text = text[:endPosition]

    # removes day bits
    while """<span class="labelone">""" in text:
        startPosition = text.find("</table>")
        # will then find if this day contains any info
        nextCloseTablePosition = text[startPosition + 3:].find("</table>") + startPosition + 3
        substring = text[startPosition + len("</table>"):nextCloseTablePosition]
        if "columnTitles" in substring:
            endPosition = text[startPosition:].find( "</tr>") + 5 + startPosition
        else:
            endPosition = text[startPosition + 3:].find("</table>") + startPosition + 3
        text = cutSectionFromText(text, startPosition, endPosition)

    return text

def extract(frameHTML):
    table = getTableFromFrame(frameHTML)

    # splits at row breaks
    rows = table.replace("</tr></tbody><tr>","</tr><tr>").split("</tr><tr>")

    for row in rows:
        row = row.replace("</td>","").replace("&amp;","&").replace("&nbsp;"," ").replace(",","")

        # splits at element break and removes first empty item from list
        event_info = row.split("<td>")[1:]

        day = event_info[0]
        subject = event_info[1]
        start_time = event_info[3]
        end_time = event_info[4]
        location = event_info[5]

        description = ""
        description += 'With: ' + event_info[6] + '\n'
        description += 'Activity: ' + event_info[1] + '\n'
        description += 'Type: ' + event_info[2] + '\n'
        description += 'Department: ' + event_info[7] + '\n'

        event = CalendarEvent(
            start=extract_datetime(day, start_time),
            end=extract_datetime(day, end_time),
            subject=subject,
            location=location,
            description=description
        )
        yield event

def extract_datetime(date, time):
    return datetime.strptime(date + " " + time, "%d %b %Y %H:%M")
