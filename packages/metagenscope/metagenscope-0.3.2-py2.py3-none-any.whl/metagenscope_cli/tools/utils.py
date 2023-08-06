"""Utility methods for CLI tool."""

import json
from functools import wraps

import click
import requests

from metagenscope_cli.config import config
from metagenscope_cli.network.token_auth import TokenAuth


def tsv_to_dict(input_tsv):
    """Convert tsv file to list of dictionaries from column name to value."""
    headerline = input_tsv.readline()
    column_names = headerline.rstrip("\n").split("\t")

    data = []

    for line in iter(input_tsv):
        parts = line.rstrip("\n").split("\t")
        row = dict(zip(column_names, parts))
        data.append(row)

    return {
        'column_names': column_names,
        'data': data,
    }


def resolve_auth_token(auth_token):
    """Resolve token provided as CLI option with saved token."""
    config_token = config.get_token()

    if auth_token is not None:
        if config_token is None:
            # Ask if we would like to save the token
            if click.confirm('Would you like to store this token for future use?'):
                config.set_token(auth_token)
            return auth_token
        elif auth_token != config_token:
            # Confirm the user would like to use a different token from config
            click.secho('The provided token is different from the stored token.', fg='yellow')
            if click.confirm('Continue with provided token?', abort=True):
                return auth_token
        return auth_token

    return config_token


def upload_command(tool_name):
    """Create upload decorator for tool name."""
    def decorator(create_payload):
        """Wrap payload generation with standard upload command."""
        @click.command()
        @click.option('--auth-token', help='JWT for authorization.')
        @click.option('--verbose', '-v', is_flag=True, help='Verbose reporting.')
        @click.argument('input-file', type=click.File('rb'))
        @wraps(create_payload)
        def wrapper(auth_token, verbose, input_file, *args, **kwargs):
            """Generate and deliver payload."""
            click.echo('Beginning upload for: {0}'.format(tool_name))

            payload = {
                'tool_name': tool_name,
                'data': create_payload(input_file, *args, **kwargs),
            }

            return deliver_payload(payload, auth_token, verbose)
        return wrapper
    return decorator
