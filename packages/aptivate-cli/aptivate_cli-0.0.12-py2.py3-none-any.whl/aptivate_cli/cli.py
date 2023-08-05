"""Command line entry point."""

import click

from aptivate_cli.cligroups.ci.commands import checks, isort, pylava, pytest
from aptivate_cli.cligroups.deployment.commands import deploy
from aptivate_cli.cligroups.metrics.commands import metrics
from aptivate_cli.cligroups.templates.commands import template


@click.group()
@click.version_option()
def main() -> None:
    """Fully automated luxury Aptivate command line interface."""


main.add_command(deploy)
main.add_command(template)
main.add_command(metrics)
main.add_command(checks)
main.add_command(pylava)
main.add_command(isort)
main.add_command(pytest)
