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
              type=click.Choice(['ical', 'csv', 'gcal']),
              help="Output format of calendar.")
@click.option('-d', '--downloader', default='chrome',
              type=click.Choice(['chrome', 'firefox']),
              help="Download driver to use.")
@click.option('--headless/--head', 'headless', default=True,
              help="Change whether the browser is run headlessly.")
@click.password_option(confirmation_prompt=False,
              help="Override password to my.bham account.")
def main(username, password, form, downloader, headless, output):
    try:
        if downloader == 'chrome':
            fr = frame.WebFrame(frame.CHROME(headless))
        elif downloader == 'firefox':
            fr = frame.WebFrame(frame.FIREFOX(headless))
        else:
            raise NotImplementedError('unsupported browser driver')

        log('downloading timetable...', Message.INFO, overwrite=True)
        source = fr.fetch(username, password)
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
        CSV(output, events)
    elif form == 'ical':
        iCalendar(output, events)
    elif form == 'gcal':
        googleCalendar(output, events)
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
