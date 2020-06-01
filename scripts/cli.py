import click

from .renderer import build_site


@click.group()
@click.version_option()
def cli():
    "Interact with the data fueling notebooks.rixx.de"


@cli.command()
def build():
    """ Build the site, putting output into _html/ """
    build_site()
