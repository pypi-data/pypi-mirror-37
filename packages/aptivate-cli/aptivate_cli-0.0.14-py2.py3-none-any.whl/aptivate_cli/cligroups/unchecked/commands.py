"""Unchecked argument convenience commands module."""

import click

from aptivate_cli import cmd


@click.command()
@click.argument('django_managepy_args', nargs=-1, type=click.UNPROCESSED)
def run(django_managepy_args: str) -> None:
    """Run a Django manage.py command under Pipenv"""
    cmd.call('pipenv run python manage.py {}'.format(
        ' '.join(django_managepy_args)
    ))
