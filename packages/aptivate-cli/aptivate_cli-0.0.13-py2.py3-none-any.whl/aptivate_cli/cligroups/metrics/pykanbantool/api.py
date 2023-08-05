"""A tiny kanbantool Python API wrapper module.

Unfortunately, there is no Python library for accessing the Kanbantool API.
Therefore, we right the least possible amount of code to get what we want.
"""

import typing
from urllib.parse import urljoin

import click
import requests

from aptivate_cli.config import Config
from aptivate_cli.settings import (
    APTIVATE_CLI_KANBANTOOL_API_TOKEN, KANBANTOOL_BASE_URI,
    KANBANTOOL_OUTREACH_BOARD_ID
)


def url_build(endpoint_uri: str) -> str:
    """Build a kanbantool API request URI."""
    return urljoin(KANBANTOOL_BASE_URI, endpoint_uri)


def fire_request(endpoint_uri: str,
                 access_token: str,
                 method: typing.Callable) -> requests.Response:
    """Fire a request to the API."""
    try:
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        response = method(
            url_build(endpoint_uri),
            headers=headers,
            allow_redirects=True,
            timeout=3,
        )
    except requests.RequestException as exception:
        message = "API request error: '{}'".format(str(exception))
        raise click.ClickException(click.style(message, fg='red'))

    if response.ok:
        return response

    message = "API request failed with status {}".format(response.status_code)
    raise click.ClickException(click.style(message, fg='red'))


def get_outreach_board(config: Config) -> typing.Dict[str, typing.Any]:
    """Retrieve a kanbantool API board.

    > https://kanbantool.com/developer/api-v3#boards
    > https://kanbantool.com/developer/api-v3#fetching-boards-details

    """
    access_token = config.get_pass_secret(APTIVATE_CLI_KANBANTOOL_API_TOKEN)
    board_uri = 'boards/{}.json'.format(KANBANTOOL_OUTREACH_BOARD_ID)
    response = fire_request(board_uri, access_token, requests.get)
    return response.json()
