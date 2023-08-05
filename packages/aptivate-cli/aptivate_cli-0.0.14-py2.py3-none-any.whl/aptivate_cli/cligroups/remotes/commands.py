"""Remote machine commands module."""

import click

from aptivate_cli import cmd
from aptivate_cli.config import Config, pass_config
from aptivate_cli.settings import (
    APTIVATE_CLI_MYSQL_PASS, APTIVATE_CLI_SSH_USER
)


@click.option(
    '--env', '-e',
    type=click.Choice(('stage', 'prod')),
    help='The remote machine',
    required=True,
)
@click.command()
@pass_config
def login(config: Config, env: str) -> None:
    """Log into a remote machine."""
    machine = 'lin-{}-{}'.format(config.project_name, env)
    config.prompt_for_values(['ssh_user'])
    command = 'ssh {}@{}.aptivate.org'.format(
        config.env_vars[APTIVATE_CLI_SSH_USER],
        machine,
    )
    cmd.call(command)


@click.option(
    '--env', '-e',
    type=click.Choice(('stage', 'prod')),
    help='The remote machine',
    required=True,
)
@click.command()
@pass_config
def shell(config: Config, env: str) -> None:
    """Run a Django shell on a remote machine."""
    machine = 'lin-{}-{}.aptivate.org'.format(config.project_name, env)
    config.prompt_for_values(['ssh_user'])
    command = (
        "ssh -t {}@{} 'cd {} && pipenv run python manage.py shell'".format(
            config.env_vars[APTIVATE_CLI_SSH_USER],
            machine,
            config.remote_project_path
        )
    )
    cmd.call(command)


@click.option(
    '--env', '-e',
    type=click.Choice(('stage', 'prod')),
    help='The remote machine',
    required=True,
)
@click.command()
@pass_config
def load(config: Config, env: str) -> None:
    """Retrieve a MySQL dump from a remote machine."""
    machine = 'lin-{}-{}.aptivate.org'.format(config.project_name, env)

    config.prompt_for_values(['ssh_user'])
    ssh_user = config.env_vars[APTIVATE_CLI_SSH_USER]

    config.prompt_for_secret_values(['mysql_pass'])
    mysql_pass = config.env_vars[APTIVATE_CLI_MYSQL_PASS]

    ssh_connect = 'ssh {}@{}'.format(ssh_user, machine)
    scp_connect = 'scp {}@{}'.format(ssh_user, machine)
    dump_path = '/tmp/{}-dump.sql'.format(config.project_name)

    dump_cmd = "{ssh} 'sudo mysqldump {db} > {path}'"
    cmd.call(dump_cmd.format(
        ssh=ssh_connect,
        db=config.project_name,
        path=dump_path
    ))

    scp_cmd = '{scp}:{remote_path} {local_path}'
    cmd.call(scp_cmd.format(
        scp=scp_connect,
        remote_path=dump_path,
        local_path=dump_path,
    ))

    load_cmd = 'mysql -uroot -p{pword} {db} < {sql}'
    cmd.call(load_cmd.format(
        pword=mysql_pass,
        db=config.project_name,
        sql=dump_path
        ), shell=True
    )
