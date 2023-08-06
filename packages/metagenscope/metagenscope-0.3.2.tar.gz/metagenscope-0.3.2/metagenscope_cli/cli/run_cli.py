"""CLI to run commands on MGS server."""

from sys import stderr
import click

from .utils import add_authorization


@click.group()
def run():
    """Run actions on the server."""
    pass


@run.group()
def middleware():
    """Run middleware."""
    pass


@middleware.command(name='group')
@add_authorization()
@click.option('-u/-n', '--uuid/--name', default=False)
@click.argument('group_name')
def group_middleware(uploader, uuid, group_name):
    """Run middleware for a group."""
    if uuid:
        group_uuid = group_name
    else:
        response = uploader.knex.get(f'/api/v1/sample_groups/getid/{group_name}')
        group_uuid = response['data']['sample_group_uuid']
        print(f'{group_name} :: {group_uuid}', file=stderr)
    response = uploader.knex.post(f'/api/v1/sample_groups/{group_uuid}/middleware', {})
    click.echo(response)


@middleware.command(name='samples')
@add_authorization()
@click.option('-u/-n', '--uuid/--name', default=False)
@click.argument('sample_names', nargs=-1)
def sample_middleware(uploader, uuid, sample_names):
    """Run middleware for a sample."""
    for sample_name in sample_names:
        if uuid:
            sample_uuid = sample_name
        else:
            response = uploader.knex.get(f'/api/v1/samples/getid/{sample_name}')
            sample_uuid = response['data']['sample_uuid']
            print(f'{sample_name} :: {sample_uuid}', file=stderr)
        try:
            response = uploader.knex.post(f'/api/v1/samples/{sample_uuid}/middleware', {})
            click.echo(response)
        except Exception:  # pylint: disable=broad-except
            click.echo('Failed.')
