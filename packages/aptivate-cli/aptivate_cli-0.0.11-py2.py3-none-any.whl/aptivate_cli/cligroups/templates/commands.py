"""Template creation commands module."""

import click

from aptivate_cli import cmd
from aptivate_cli.settings import PLAY_TEMPLATE_URL, ROLE_TEMPLATE_URL


@click.option(
    '--type', '-t',
    type=click.Choice(('play', 'role',)),
    help='The type of template',
    required=True,
)
@click.command()
def template(type: str) -> None:
    """Generate a new template."""
    if type == 'play':
        cmd.clone_template(PLAY_TEMPLATE_URL)
    elif type == 'role':
        cmd.clone_template(ROLE_TEMPLATE_URL)
    else:
        message = click.style('Unknown type', fg='red')
        raise click.ClickException(message)
