"""A module for generating configuration based on convention.

For each command that needs a configuration to run, we hand it over to the
command logic by using the `@pass_config` decorator that Click provides. The
`Config` objects works hard to accumulate all the configuration context that a
command will need by basing decisions off of our naming and location
conventions.

"""

import typing
from os import environ, getcwd, listdir
from os.path import abspath, basename, join
from subprocess import CalledProcessError

import click

from aptivate_cli.settings import (
    ANSIBLE_HOME_DIRECTORY, ANSIBLE_INVENTORIES_DIRECTORY,
    ANSIBLE_INVENTORY_FILE, ANSIBLE_PLAYBOOK_FILE, ANSIBLE_PLAYBOOKS_DIRECTORY,
    ANSIBLE_REQUIREMENTS_FILE, ANSIBLE_ROLE_PATHS, ANSIBLE_VAULT_FILE,
    APTIVATE_CLI_MYSQL, APTIVATE_CLI_PASS_DIR, APTIVATE_CLI_SUDO,
    PROJECT_PLAY_REPOSITORY_URL
)


class Config():
    """The command configuration."""

    MANDATORY_ENV_VARS: typing.Dict[str, typing.Any] = {
        APTIVATE_CLI_PASS_DIR: None,
    }

    OPTIONAL_ENV_VARS: typing.Dict[str, typing.Any] = {
        APTIVATE_CLI_MYSQL: None,
        APTIVATE_CLI_SUDO: None,
    }

    def __init__(self, ) -> None:
        """Initialise the object."""
        self.env_vars: typing.Dict[str, typing.Any] = {
            **self.MANDATORY_ENV_VARS,
            **self.OPTIONAL_ENV_VARS
        }

    def django_checks(selfself) -> None:
        """Run Django related sanity checks."""
        cwd_contents = listdir(abspath(getcwd()))
        if 'manage.py' not in cwd_contents:
            message = "No 'manage.py' in current directory"
            raise click.ClickException(click.style(message, fg='red'))

    def env_var_checks(self) -> None:
        """Run environment related sanity checks."""
        for env_var_key in self.MANDATORY_ENV_VARS:
            if not environ.get(env_var_key, False):
                message = "No '{}' exposed in environment".format(env_var_key)
                raise click.ClickException(click.style(message, fg='red'))

    def prompt_for_values(self,
                          variables: typing.List[str],
                          hide_input: bool = False
                          ) -> typing.Dict[str, typing.Any]:
        """Ask for values using the Click prompt."""
        PROMPT_MAPPINGS = {
            'mysql': 'MySQL root password required',
            'sudo': 'Sudo password required',
        }

        if not all(var in PROMPT_MAPPINGS for var in variables):
            message = click.secho('Missing prompt mapping', fg='red')
            raise click.ClickException(message)

        for variable in variables:
            env_var_marker = 'APTIVATE_CLI_{}'.format(variable.upper())
            env_var_value = environ.get(env_var_marker, None)

            if env_var_value is not None:
                self.env_vars[env_var_marker] = env_var_value
                continue

            self.env_vars[env_var_marker] = click.prompt(
                PROMPT_MAPPINGS[variable],
                hide_input=hide_input
            )

        return self.env_vars

    def prompt_for_secret_values(self,
                                 variables: typing.List[str],
                                 hide_input: bool = True
                                 ) -> typing.Dict[str, typing.Any]:
        """Ask for values using the Click secret prompt."""
        self.prompt_for_values(variables, hide_input=hide_input)
        return self.env_vars

    @property
    def project_name(self):
        """The name of the project."""
        return basename(abspath(getcwd()))

    @property
    def project_play_url(self):
        """The project play Git URL."""
        return PROJECT_PLAY_REPOSITORY_URL.format(self.project_name)

    @property
    def project_play_path(self):
        """The project play path."""
        return join(
            abspath(getcwd()),
            self.ansible_home_path,
            '{}-play'.format(self.project_name)
        )

    def playbook_path(self, env: str) -> str:
        """The project playbook path."""
        return join(
            abspath(getcwd()),
            self.ansible_home_path,
            '{}-play'.format(self.project_name),
            ANSIBLE_PLAYBOOKS_DIRECTORY,
            env,
            ANSIBLE_PLAYBOOK_FILE

        )

    def get_pass_secret(self, password: str) -> str:
        """Retrieve a password from the pass store."""
        from aptivate_cli.cmd import call

        command = 'pass show {}'.format(password)
        env = {'PASSWORD_STORE_DIR': environ[APTIVATE_CLI_PASS_DIR]}

        try:
            looked_up_password: bytes = call(command, env=env)
            return looked_up_password.decode('utf-8').strip()
        except CalledProcessError:
            message = "Cannot retrieve '{}'".format(password)
            raise click.ClickException(click.style(message, fg='red'))

    @property
    def inventory_path(self) -> str:
        """The project inventory path."""
        return join(
            abspath(getcwd()),
            self.ansible_home_path,
            '{}-play'.format(self.project_name),
            ANSIBLE_INVENTORIES_DIRECTORY,
            ANSIBLE_INVENTORY_FILE,

        )

    @property
    def role_paths(self) -> typing.List[str]:
        """The project roles path."""
        return [
            join(
                abspath(getcwd()),
                self.ansible_home_path,
                '{}-play'.format(self.project_name),
                role_path
            )
            for role_path in ANSIBLE_ROLE_PATHS
        ]

    @property
    def ansible_home_path(self):
        """The home directory for Ansible project files."""
        return ANSIBLE_HOME_DIRECTORY

    @property
    def galaxy_requirements_file(self):
        """The name by convention for the galaxy requirements file."""
        return ANSIBLE_REQUIREMENTS_FILE

    @property
    def vault_file(self):
        """The name by convention for the vault password file."""
        return join(
            abspath(getcwd()),
            self.ansible_home_path,
            '{}-play'.format(self.project_name),
            ANSIBLE_VAULT_FILE,
        )


pass_config = click.make_pass_decorator(Config, ensure=True)
