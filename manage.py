#!/usr/bin/env python
import click
from pte.scrapers.core import run_all
from pte import model_storage
from pte.gcal.sync import sync as gcal_sync


@click.group()
def cli():
    pass


@cli.command()
def scrape():
    """
    Scrape the content of remote sources and store them locally as JSON files
    """
    run_all()


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
