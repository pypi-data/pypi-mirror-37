"""Molecule helper commands module."""

import click

from aptivate_cli import cmd
from aptivate_cli.config import Config, pass_config


@click.option(
    '--driver', '-d',
    type=click.Choice(('docker', 'linode',)),
    help='The type of Molecule driver',
    required=True,
)
@click.option(
    '--name', '-n',
    help='The name of the Molecule scenario',
    default='default',
    show_default=True,
)
@click.command()
@pass_config
def scenario(config: Config, driver: str, name: str) -> None:
    """Generate a new Molecule scenario."""
    arguments = '-r {} -s {} -d {}'.format(config.project_name, name, driver)
    command = 'pipenv run molecule init scenario {} '.format(arguments)
    cmd.call(command)
