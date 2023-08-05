"""Gitlab CI commands module."""

from subprocess import CalledProcessError

import click

from aptivate_cli.config import Config, pass_config


@click.command()
@pass_config
def checks(config: Config) -> None:
    """Gitlab CI Django checks."""
    from aptivate_cli import cmd

    config.django_checks()

    commands = [
        'pipenv run python manage.py check',
        'pipenv run python manage.py makemigrations --check',
    ]

    for command in commands:
        try:
            cmd.call(command)
        except CalledProcessError as check_exception:
            message = str(check_exception)
            raise click.ClickException(click.style(message, fg='red'))


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('pylava_args', nargs=-1, type=click.UNPROCESSED)
@pass_config
def pylava(config: Config, pylava_args: str) -> None:
    """Gitlab CI Pylava runner.

    Accepts Pylava arguments as you might expect:

    $ apc pylava -o=setup.cfg
    """
    from aptivate_cli import cmd

    config.django_checks()

    try:
        cmd.call('pipenv run pylava {}'.format(' '.join(pylava_args)))
    except CalledProcessError as check_exception:
        message = str(check_exception)
        raise click.ClickException(click.style(message, fg='red'))


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('isort_args', nargs=-1, type=click.UNPROCESSED)
@pass_config
def isort(config: Config, isort_args: str) -> None:
    """Gitlab CI Isort runner.

    Accepts Isort arguments as you might expect:

    $ apc isort -sp=setup.cfg
    """
    from aptivate_cli import cmd

    config.django_checks()

    try:
        cmd.call('pipenv run isort'.format(' '.join(isort_args)))
    except CalledProcessError as check_exception:
        message = str(check_exception)
        raise click.ClickException(click.style(message, fg='red'))


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('pytest_args', nargs=-1, type=click.UNPROCESSED)
@pass_config
def pytest(config: Config, pytest_args) -> None:
    """Gitlab CI Pytest runner.

    Accepts Pytest arguments as you might expect:

    $ apc test -v --cov
    """
    config.django_checks()

    try:
        cmd.call('pipenv run pytest {}'.format(' '.join(pytest_args)))
    except CalledProcessError as check_exception:
        message = str(check_exception)
        raise click.ClickException(click.style(message, fg='red'))
