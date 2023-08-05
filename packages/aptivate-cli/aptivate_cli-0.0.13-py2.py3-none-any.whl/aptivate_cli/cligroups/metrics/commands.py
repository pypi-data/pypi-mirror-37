"""Metric commands module."""

from datetime import datetime as dt
from datetime import timedelta
from typing import Dict

import click
from click_datetime import Datetime

from aptivate_cli.cligroups.metrics.outreach import (
    get_new_conversations, get_won_conversations
)
from aptivate_cli.cligroups.metrics.pykanbantool.api import get_outreach_board
from aptivate_cli.config import Config, pass_config

DATETIME = Datetime(format='%d/%m/%y')
TODAY = dt.now()
LAST_MONTH = dt.now() - timedelta(days=30)


@click.group()
def metrics() -> None:
    """Retrieve Aptivate related metrics."""
    pass


@click.option(
    '--start', '-s',
    type=DATETIME,
    default=LAST_MONTH,
    help='The start date',
    required=True,
    show_default=True,
)
@click.option(
    '--end', '-e',
    type=DATETIME,
    default=TODAY,
    help='The end date',
    required=True,
    show_default=True,
)
@metrics.command()
@pass_config
def outreach(config: Config,
             start: dt,
             end: dt) -> Dict[str, int]:
    """Outreach metrics."""
    config.env_var_checks()

    board = get_outreach_board(config)

    # FIXME: Implement this ...
    new_conversations = get_new_conversations(start, end, board)
    won_conversations = get_won_conversations(new_conversations)

    return {
        'new_conversations': len(new_conversations),
        'won_conversations': len(won_conversations),
    }
