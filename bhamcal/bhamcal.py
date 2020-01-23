import click
import sys

from . import frame
from .extractor import extract
from .utils import log
from .utils import Message

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
@click.option('-d', '--downloader', default='native',
              type=click.Choice(['native', 'chrome', 'firefox']),
              help="Download driver to use.")
@click.option('--headless/--head', 'headless', default=True,
              help="Change whether the browser is run headlessly.")
@click.option('--colors/--no-colors', default=False,
              help="Enable module-wise color outputs (only gcal)")
@click.password_option(confirmation_prompt=False,
              help="Override password to my.bham account.")
def main(username, password, form, downloader, headless, output, colors):
    try:
        if downloader == 'native':
            fr = frame.NativeFrame()
        elif downloader == 'chrome':
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

    log(f'converting calendar to {form}...', Message.INFO)
    if form == 'csv':
        CSV(output, events)
    elif form == 'ical':
        iCalendar(output, events)
    elif form == 'gcal':
        googleCalendar(output, events, use_colors=colors)
    else:
        raise ValueError("invalid output format")
    log(f'converted calendar to {form}', Message.INFO)

    log(f'written calendar to {output}', Message.SUCCESS)
    log()