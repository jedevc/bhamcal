# Birmingham Uni timetable extractor

The University of Birmingham has a lovely service for accessing timeatables
that is completely incompatible with any reasonable system. This is a simple
command line tool to extract the data from my.bham and generate something
compatible with a reasonable system.

This project is inspired (and takes a bit of code from) [Tom Moses](https://github.com/tomhmoses)'s
work on [OnlineBhamTimetableConverter][timetable-converter]. It's a great
project, however, I'm generally unhappy about having to give my password off
to third-party services, and I just need a simple command line tool.

## Usage

At the moment, there is no way to install bhamcal system-wide, so you'll have
to download and run it from the repository. Note that bhamcal uses
[Pipenv](https://pipenv.readthedocs.io/en/latest/).

    $ git clone https://github.com/jedevc/bhamcal.git
    $ cd bhamcal
    $ pipenv shell

To generate a calendar in CSV format:

    $ python -m bhamcal <username> -o calendar.csv

To generate a calendar in iCal format:

    $ python -m bhamcal <username> -f ical -o calendar.ics

For other options, see the help:

    $ python -m bhamcal --help

## License

Like [OnlineBhamTimetableConverter][timetable-converter], this project is
licensed under the GPLv3. Enjoy! :tada:

[timetable-converter]: https://github.com/tomhmoses/OnlineBhamTimetableConverter