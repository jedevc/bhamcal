def CSV(filename, events):
    with open(filename, 'w') as output:
        header = [
            "Start date",
            "End date",
            "Subject",
            "Start Time",
            "End Time",
            "Location",
            "Description"
        ]
        output.write(','.join(header) + '\n')

        for event in events:
            day = event.start.strftime("%D")
            parts = [
                day,                           # Start date
                day,                           # End date
                event.subject,                 # Subject
                event.start.strftime("%R"),    # Start Time
                event.end.strftime("%R"),      # End Time
                event.location,                # Location
                '"' + event.description + '"'  # Description
            ]
            line = ','.join(parts)
            output.write(line + '\n')
