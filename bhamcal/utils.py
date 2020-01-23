import click
import sys

class Message:
    SUCCESS = 'green'
    INFO    = 'blue'
    ERROR   = 'red'

def log(message='', level=None, overwrite=False):
    # don't prefix empty messages
    if len(message.strip()) != 0:
        message = '[*] ' + message

    # work out overwriting
    if overwrite and log.overwrite_next:
        message = '\r' + message
    elif overwrite:
        click.echo(err=True)
        log.overwrite_next = True
    elif log.overwrite_next:
        message = '\r' + message
        log.overwrite_next = False
    else:
        click.echo(err=True)

    click.secho(message, fg=level, nl=False, err=True)

log.overwrite_next = False