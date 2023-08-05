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

    Passes default arguments for convenience:

      * -o=setup.cfg

    Accepts arguments as you might expect:

    $ apc pylava --async --verbose

    Passing arguments overrides the defaults.
    """
    from aptivate_cli import cmd

    config.django_checks()

    default_args = '-o setup.cfg'
    user_args = ' '.join(pylava_args)

    try:
        cmd.call('pipenv run pylava {}'.format(
            user_args if user_args else default_args
        ))
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

    Passes default arguments for covenience:

      * -q -rc -c -df -sp setup.cfg

    Accepts arguments as you might expect:

    $ apc isort -rc -y -sp setup.cfg

    Passing arguments overrides the defaults.
    """
    from aptivate_cli import cmd

    config.django_checks()

    default_args = '-q -rc -c -df -sp setup.cfg'
    user_args = ' '.join(isort_args)

    try:
        cmd.call('pipenv run isort {} '.format(
            user_args if user_args else default_args
        ))
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

    Passes default arguments for covenience:

      * -v

    Accepts arguments as you might expect:

    $ apc pytest --cov

    Passing arguments overrides the defaults.
    """
    from aptivate_cli import cmd

    config.django_checks()

    default_args = '-v'
    user_args = ' '.join(pytest_args)

    try:
        cmd.call('pipenv run pytest {}'.format(
            user_args if user_args else default_args
        ))
    except CalledProcessError as check_exception:
        message = str(check_exception)
        raise click.ClickException(click.style(message, fg='red'))
