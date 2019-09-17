import click

from .frame import Frame
from .extractor import extract

@click.command("bhamcal")
@click.argument('username')
@click.option('-o', '--output', default='-', type=click.File('w'))
@click.password_option()
def main(username, password, output):
    fr = Frame(username, password)
    source = fr.extract(fr.CHROME)

    calendar = extract(source)

    output.write(calendar)

if __name__ == "__main__":
    main()