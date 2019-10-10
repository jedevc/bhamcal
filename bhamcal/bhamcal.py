import click
import sys

from . import frame
from .extractor import extract

from .output.csv import CSV
from .output.icalendar import iCalendar
from .output.gcal import googleCalendar

@click.command("bhamcal")
@click.argument('username')
@click.option('-o', '--output', required=True,
              help="File to output the results to.")
@click.option('-f', '--format', 'form', default='ical',
              type=click.Choice(['csv', 'ical', 'gcal']),
              help="Output format of calendar.")
@click.option('--headless/--head', 'headless', default=True,
              help="Change whether the browser is run headlessly.")
@click.password_option(confirmation_prompt=False,
              help="Override password to my.bham account.")
def main(username, password, form, headless, output):
    fr = frame.Frame(username, password)
    log('downloading timetable...', Message.INFO, overwrite=True)
    try:
        browser = fr.CHROME(headless)
        source = fr.fetch(browser)
    except frame.FrameFetchError:
        log('failed to download timetable', Message.ERROR)
        log()
        return
    log(f'downloaded timetable for {username}', Message.INFO)

    events = list(extract(source))
    events.sort(key=lambda x: x.start)
    log(f'extracted {len(events)} events', Message.INFO)

    log(f'converting calendar to {form}...', Message.INFO, overwrite=True)
    if form == 'csv':
        calendar = CSV(output, events)
    elif form == 'ical':
        calendar = iCalendar(output, events)
    elif form == 'gcal':
        calendar = googleCalendar(output, events)
    else:
        raise ValueError("invalid output format")
    log(f'converted calendar to {form}', Message.INFO)

    log(f'written calendar to {output}', Message.SUCCESS)
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
        click.echo(err=True)
        log.overwrite_next = True
    elif log.overwrite_next:
        message = '\r' + message
        log.overwrite_next = False
    else:
        click.echo(err=True)

    click.secho(message, fg=level, nl=False, err=True)

log.overwrite_next = False
