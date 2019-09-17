# Birmingham Uni timtable extractor

The University of Birmingham has a lovely service for accessing timeatables
that is completely incompatible with any reasonable system. This is a simple
command line tool to extract the data from my.bham and generate something
compatible with a reasonable system.

This project is inspired (and takes a bit of code from) [Tom Moses](https://github.com/tomhmoses)'s
work on [OnlineBhamTimetableConverter][timetable-converter]. It's a great
project, however, I'm generally unhappy about having to give my password off
to third-party services, and I just need a simply command line tool.

## Usage

For a command line tool, bhamcal is very easy to use.

    $ pipenv shell
    $ python -m bhamcal --help

## License

Like [timetable-converter][timetable-converter], this project is licensed
under the GPLv3. Enjoy! :tada:

[timetable-converter]: https://github.com/tomhmoses/OnlineBhamTimetableConverter