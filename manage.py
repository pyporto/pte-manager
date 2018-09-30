#!/usr/bin/env python
import click
from pte.scrapers.core import run_scraper, scrapers, run_all
from pte import model_storage
from pte.gcal.sync import sync as gcal_sync


@click.group()
def cli():
    pass


@cli.command()
def list_scrapers():
    """
    Scrape the content of remote sources and store them locally as JSON files
    """
    for name in sorted(scrapers.keys()):
        click.echo(name)


@click.argument('scraper_names', nargs=-1)
@cli.command()
def scrape(scraper_names):
    """
    Scrape the content of remote sources and store them locally as JSON files
    """
    if not scraper_names:
        return run_all()
    for name in scraper_names:
        run_scraper(name)


@cli.command()
def status():
    """
    Show the status of the model storage
    """
    model_storage.status()


@cli.command()
def sync_github():
    """
    Commit changes in JSON files and push them to the upstream
    """
    model_storage.commit()
    model_storage.push()


@cli.command()
def sync_gcal():
    """
    Update Google Calendars from local JSON files
    """
    gcal_sync()


if __name__ == '__main__':
    cli()
