"""A module for shell commands."""

import shlex
import subprocess
import typing
from os import getcwd
from os.path import abspath, exists

import click
from ansible_runner.interface import run

from aptivate_cli.config import Config
from aptivate_cli.settings import (
    APTIVATE_CLI_MYSQL_PASS, APTIVATE_CLI_SUDO_PASS
)


def call(command: str,
         cwd: str = None,
         env: typing.Dict[str, str] = None
         ) -> typing.Any:
    """A handler for command running with nice colours."""
    explained = (
        'cd {} && {}'.format(cwd, command)
        if cwd is not None else command
    )
    click.secho(explained, fg='green')

    command_kwargs: typing.Dict[str, typing.Any] = {}
    if env:
        command_kwargs['env'] = env
    if cwd:
        command_kwargs['cwd'] = cwd

    return_code = subprocess.call(
        shlex.split(command),
        **command_kwargs
    )

    if return_code != 0:
        raise subprocess.CalledProcessError(
            returncode=return_code,
            cmd=command
        )

    return return_code


def clone_template(template, no_input=False) -> None:
    """Clone a template."""
    command = (
        'cookiecutter -f --no-input {}'
        if no_input else 'cookiecutter -f {}'
    )
    call(command.format(template))


def create_ansible_home(config) -> None:
    """Create the Ansible home directory."""
    if not exists(config.ansible_home_path):
        call('mkdir {}'.format(config.ansible_home_path))


def git_clone_project_play(config: Config) -> None:
    """Clone the project play."""
    if not exists(config.project_play_path):
        command = 'git clone {}'.format(config.project_play_url)
        call(command, cwd=config.ansible_home_path)


def pipenv_install_project_play(config: Config) -> None:
    """Run a Pipenv install on the project play."""
    call('pipenv sync', cwd=config.project_play_path)


def galaxy_install_project_play(config: Config) -> None:
    """Run an ansible-galaxy requirements install."""
    command = 'pipenv run ansible-galaxy install -r {}'.format(
        config.galaxy_requirements_file
    )
    call(command, cwd=config.project_play_path)


def playbook_run_project_play(config: Config, env: str) -> None:
    """Run the project playbook based on the environment."""
    runner_kwargs: typing.Dict[str, typing.Any] = dict(
        playbook=config.playbook_path(env),
        inventory=config.inventory_path,
        roles_path=config.role_paths,
        verbosity=2,
    )

    extravars: typing.Dict[str, str] = {}

    if env == 'dev':
        config.prompt_for_secret_values(['sudo_pass', 'mysql_pass'])
        extravars = {
            'django_dev_project_root': abspath(getcwd()),
            'django_dev_project_name': config.project_name,
            'ansible_become_pass': config.env_vars[APTIVATE_CLI_SUDO_PASS],
            'mysql_root_password': config.env_vars[APTIVATE_CLI_MYSQL_PASS],
        }
    else:
        config.env_var_checks()
        extravars['cmdline'] = '--vault-password-file {}'.format(config.vault_file)

    if extravars:
        runner_kwargs['extravars'] = extravars

    run(**runner_kwargs)
