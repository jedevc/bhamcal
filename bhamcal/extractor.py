def changeDateFormat(originalDate, monthDict):
    #start with 01 Oct 2018
    #end with 10/01/2018
    bits = originalDate.split(" ")
    newDate = monthDict[bits[1]]+"/"+bits[0]+"/"+bits[2]
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
    csv = "Start date,End date,Subject,Start Time,End Time,Location,Description"
    monthDict = {
        "Jan":"01",
        "Feb":"02",
        "Mar":"03",
        "Apr":"04",
        "May":"05",
        "Jun":"06",
        "Jul":"07",
        "Aug":"08",
        "Sep":"09",
        "Oct":"10",
        "Nov":"11",
        "Dec":"12"
    }

    wholeTable = getTableFromFrame(frameHTML)

    #splits at row breaks
    listOfRows = wholeTable.replace("</tr></tbody><tr>","</tr><tr>").split("</tr><tr>")

    temp = ""
    for eachEvent in listOfRows:
        eachEvent = eachEvent.replace("</td>","").replace("&amp;","&").replace("&nbsp;"," ").replace(",","")
        #splits at element break and removes first empty item from list
        temp += "\n\n" + eachEvent.split("<td>")[0]
        eventInfoList = eachEvent.split("<td>")[1:]
        csvLine = "\n"
        #adds start and end date (which are the same)
        for count in range(2):
            csvLine += changeDateFormat(eventInfoList[0],monthDict) + ","
        #adds basic info
        for number in [1,3,4,5]:
            csvLine += eventInfoList[number] + ","
        #adds description
        csvLine += '"'
        if eventInfoList[6].replace(" ","") != "":
            csvLine += 'With: ' + eventInfoList[6] + '\n'
        csvLine += 'Activity: ' + eventInfoList[1] + '\n'
        csvLine += 'Type: ' + eventInfoList[2] + '\n'
        csvLine += 'Department: ' + eventInfoList[7] + '\n'
        csvLine += '"'

        csv += csvLine

    return csv
