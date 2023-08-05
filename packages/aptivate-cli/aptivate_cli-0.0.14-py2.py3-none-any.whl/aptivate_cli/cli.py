"""Command line entry point."""

import click

from aptivate_cli.cligroups.ci.commands import checks, isort, pylava, pytest
from aptivate_cli.cligroups.deployment.commands import deploy
from aptivate_cli.cligroups.metrics.commands import metrics
from aptivate_cli.cligroups.molecule.commands import scenario
from aptivate_cli.cligroups.remotes.commands import load, login, shell
from aptivate_cli.cligroups.templates.commands import template
from aptivate_cli.cligroups.unchecked.commands import run
from aptivate_cli.config import Config, pass_config


@click.group()
@click.version_option()
@pass_config
def main(config: Config) -> None:
    """
    \b
      __ _ _ __ | |_(_)_   ____ _| |_ ___        ___| (_)
     / _` | '_ \| __| \ \ / / _` | __/ _ \_____ / __| | |
    | (_| | |_) | |_| |\ V / (_| | ||  __/_____| (__| | |
     \__,_| .__/ \__|_| \_/ \__,_|\__\___|      \___|_|_|
          |_|
    """  # noqa


# Django deployment commands #
main.add_command(deploy)

# Template commands #
main.add_command(template)

# Metrics commands #
main.add_command(metrics)

# Gitlab CI commands #
main.add_command(checks)
main.add_command(pylava)
main.add_command(isort)
main.add_command(pytest)

# Molecule commands #
main.add_command(scenario)

# Remote commands #
main.add_command(login)
main.add_command(shell)
main.add_command(load)

# Unchecked argument commands #
main.add_command(run)
