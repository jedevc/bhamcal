import click
import sys

from . import frame
from .extractor import extract

from .output.csv import CSV
from .output.icalendar import iCalendar

@click.command("bhamcal")
@click.argument('username')
@click.option('-o', '--output', default='-', type=click.File('w'),
              help="File to output the results to.")
@click.option('-f', '--format', 'form', default='csv',
              type=click.Choice(['csv', 'ical']),
              help="Output format of calendar.")
@click.option('--all', 'week', flag_value=frame.WeekSelection.ALL,
              default=True, help="Process all available events (default).")
@click.option('--this-week', 'week', flag_value=frame.WeekSelection.CURRENT,
              help="Process only events from this week.")
@click.option('--next-week', 'week', flag_value=frame.WeekSelection.NEXT,
              help="Process only events from next week.")
@click.password_option(confirmation_prompt=False,
              help="Override password to my.bham account.")
def main(username, password, form, output, week):
    fr = frame.Frame(username, password, week)
    log('downloading timetable...', Message.INFO, overwrite=True)
    try:
        source = fr.fetch(fr.CHROME)
    except frame.FrameFetchError:
        log('failed to download timetable', Message.ERROR)
        log()
        return

    log(f'downloaded timetable for {username}', Message.INFO)

    events = list(extract(source))
    log(f'extracted {len(events)} events', Message.INFO)

    if form == 'csv':
        calendar = CSV(events)
    elif form == 'ical':
        calendar = iCalendar(events)
    else:
        raise ValueError("invalid output format")
    log(f'converted calendar to {form}', Message.INFO)

    output.write(calendar)
    log(f'written calendar to {output.name}', Message.SUCCESS)
    log()

class Message:
    SUCCESS = 'green'
    INFO    = 'blue'
    ERROR   = 'red'

def log(message='', level=None, overwrite=False):
    # don't prefix empty messages
    if len(message.strip()) != 0:
        message = '[*] ' + message

    # work out overwriting
    if overwrite:
        log.overwrite_next = True
    elif log.overwrite_next:
        message = '\r' + message
        log.overwrite_next = False
    else:
        click.echo(err=True)

    click.secho(message, fg=level, nl=False, err=True)

log.overwrite_next = False
