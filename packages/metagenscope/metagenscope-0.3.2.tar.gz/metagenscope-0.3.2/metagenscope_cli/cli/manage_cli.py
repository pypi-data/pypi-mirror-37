"""CLI to upload data to a MetaGenScope Server."""

from sys import stderr

import click

from .utils import add_authorization


@click.group()
def manage():
    """Manage MetaGenScope data."""
    pass


@manage.command()
@add_authorization()
@click.argument('group_uuid')
def delete_group(uploader, group_uuid):
    """Delete a sample group by uuid."""
    try:
        response = uploader.knex.delete(f'/api/v1/sample_groups/{group_uuid}')
        click.echo(response)
    except Exception:  # pylint:disable=broad-except
        print(f'[manage-delete_group-error] {group_uuid}', file=stderr)
