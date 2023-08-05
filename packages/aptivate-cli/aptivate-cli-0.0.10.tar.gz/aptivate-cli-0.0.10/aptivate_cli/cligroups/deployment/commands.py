"""Django deployment commands module."""

import click

from aptivate_cli import cmd
from aptivate_cli.config import Config, pass_config


@click.option(
    '--env', '-e',
    type=click.Choice(('dev', 'stage', 'prod')),
    help='The target environment',
    required=True,
    default='dev',
    show_default=True,
)
@click.command()
@pass_config
def deploy(config: Config, env: str) -> None:
    """Deploy a Django application."""
    config.django_checks()
    config.env_var_checks()

    cmd.create_ansible_home(config)
    cmd.git_clone_project_play(config)
    cmd.pipenv_install_project_play(config)
    cmd.galaxy_install_project_play(config)
    cmd.playbook_run_project_play(config, env)
