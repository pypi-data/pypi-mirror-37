"""Outreach specific metrics wrangling module."""

import datetime
import typing

import click


def get_new_conversations(start: datetime.datetime,
                          end: datetime.datetime,
                          board: typing.Dict[str, typing.Any]) -> int:
    """How many new conversations have we had in some time period?"""
    message = click.style('Not Implemented yet', fg='red')
    raise click.ClickException(message)


def get_won_conversations(conversations: typing.Dict[str, typing.Any]) -> int:
    """How many new conversations ended up being Won."""
    message = click.style('Not Implemented yet', fg='red')
    raise click.ClickException(message)
