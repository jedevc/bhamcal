import click

from .frame import Frame, WeekSelection
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
@click.option('--all', 'week', flag_value=WeekSelection.ALL, default=True,
              help="Process all available events (default).")
@click.option('--this-week', 'week', flag_value=WeekSelection.CURRENT,
              help="Process only events from this week.")
@click.option('--next-week', 'week', flag_value=WeekSelection.NEXT,
              help="Process only events from next week.")
@click.password_option(
              help="Override password to my.bham account.")
def main(username, password, form, output, week):
    fr = Frame(username, password, week)
    source = fr.extract(fr.CHROME)

    events = extract(source)

    if form == 'csv':
        calendar = CSV(events)
    elif form == 'ical':
        calendar = iCalendar(events)
    else:
        raise ValueError("invalid output format")

    output.write(calendar)
