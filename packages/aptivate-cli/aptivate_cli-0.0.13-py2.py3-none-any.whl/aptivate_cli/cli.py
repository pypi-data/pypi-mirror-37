"""Command line entry point."""

import click

from aptivate_cli import cmd
from aptivate_cli.cligroups.ci.commands import checks, isort, pylava, pytest
from aptivate_cli.cligroups.deployment.commands import deploy
from aptivate_cli.cligroups.metrics.commands import metrics
from aptivate_cli.cligroups.molecule.commands import scenario
from aptivate_cli.cligroups.remotes.commands import load, login, shell
from aptivate_cli.cligroups.templates.commands import template
from aptivate_cli.config import Config, pass_config


@click.group(invoke_without_command=True)
@click.version_option()
@click.argument('django_managepy_args', nargs=-1, type=click.UNPROCESSED)
@pass_config
def main(config: Config, django_managepy_args: str) -> None:
    """
    \b
      __ _ _ __ | |_(_)_   ____ _| |_ ___        ___| (_)
     / _` | '_ \| __| \ \ / / _` | __/ _ \_____ / __| | |
    | (_| | |_) | |_| |\ V / (_| | ||  __/_____| (__| | |
     \__,_| .__/ \__|_| \_/ \__,_|\__\___|      \___|_|_|
          |_|

    For the entire command reference, please see:

    > https://git.coop/aptivate/internal-tools/aptivate-cli/blob/master/docs/commands.md

    """  # noqa
    config.django_checks()
    command = 'pipenv run python manage.py {}'
    cmd.call(command.format(' '.join(django_managepy_args)))


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
