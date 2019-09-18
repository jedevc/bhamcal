from .event import Event
from datetime import datetime

def changeDateFormat(originalDate):
    bits = originalDate.split(" ")
    newDate = MONTHS[bits[1]]+"/"+bits[0]+"/"+bits[2]
    return newDate

def cutSectionFromText(text,startPosition, endPosition):
    text1 = text[:startPosition]
    text2 = text[endPosition:]
    return text1 + text2

def getTableFromFrame(text):
    text =  text.replace('\n', '').replace('\r', '')
    #cuts off top
    startPosition = text.find("""<p><span class="labelone">""") - len("</table>")
    text = text[startPosition:]
    #cuts off bottom
    endPosition = text.find("""<table class="footer-border-args" """)
    text = text[:endPosition]

    #removes day bits
    while """<span class="labelone">""" in text:
        startPosition = text.find("</table>")
        #will then find if this day contains any info
        nextCloseTablePosition = text[startPosition+3:].find("</table>")+startPosition+3
        substring = text[startPosition+len("</table>"):nextCloseTablePosition]
        if "columnTitles"  in substring:
            endPosition = text[startPosition:].find("</tr>") + 5 + startPosition
        else:
            endPosition = text[startPosition+3:].find("</table>")+startPosition+3

        text = cutSectionFromText(text,startPosition,endPosition)
    return text

def extract(frameHTML):
    wholeTable = getTableFromFrame(frameHTML)

    csv = "Start date,End date,Subject,Start Time,End Time,Location,Description"

    # splits at row breaks
    listOfRows = wholeTable.replace("</tr></tbody><tr>","</tr><tr>").split("</tr><tr>")

    for eachEvent in listOfRows:
        eachEvent = eachEvent.replace("</td>","").replace("&amp;","&").replace("&nbsp;"," ").replace(",","")

        # splits at element break and removes first empty item from list
        eventInfoList = eachEvent.split("<td>")[1:]

        day = changeDateFormat(eventInfoList[0])
        subject = eventInfoList[1]
        start_time = eventInfoList[3]
        end_time = eventInfoList[4]
        location = eventInfoList[5]

        description = ""
        description += 'With: ' + eventInfoList[6] + '\n'
        description += 'Activity: ' + eventInfoList[1] + '\n'
        description += 'Type: ' + eventInfoList[2] + '\n'
        description += 'Department: ' + eventInfoList[7] + '\n'

        entry = ','.join([day, day, subject, start_time, end_time, location, '"' + description + '"'])
        csv += entry + '\n'

    return csv

MONTHS = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}