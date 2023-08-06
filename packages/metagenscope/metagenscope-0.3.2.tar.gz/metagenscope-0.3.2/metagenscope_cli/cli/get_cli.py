"""CLI to get data from a MetaGenScope Server."""

from sys import stderr

import click
from requests.exceptions import HTTPError

from .utils import add_authorization


@click.group()
def get():
    """Get data from the server."""
    pass


@get.command(name='orgs')
@add_authorization()
def get_orgs(uploader):
    """Get a list of organizations."""
    try:
        response = uploader.knex.get('/api/v1/organizations')
        click.echo(response)
    except HTTPError as exc:
        print(f'{exc}', file=stderr)


@get.group()
def uuids():
    """Get UUIDs from the server."""
    pass


def report_uuid(name, uuid):
    """Report a uuid to the user."""
    click.echo(f'{name}\t{uuid}')


@uuids.command(name='samples')
@add_authorization()
@click.argument('sample_names', nargs=-1)
def sample_uuids(uploader, sample_names):
    """Get UUIDs for the given sample names."""
    for sample_name in sample_names:
        response = uploader.knex.get(f'/api/v1/samples/getid/{sample_name}')
        report_uuid(response['data']['sample_name'],
                    response['data']['sample_uuid'])


@uuids.command(name='groups')
@add_authorization()
@click.argument('sample_group_names', nargs=-1)
def sample_group_uuids(uploader, sample_group_names):
    """Get UUIDs for the given sample groups."""
    for sample_group_name in sample_group_names:
        try:
            response = uploader.knex.get(f'/api/v1/sample_groups/getid/{sample_group_name}')
            report_uuid(response['data']['sample_group_name'],
                        response['data']['sample_group_uuid'])
        except Exception:  # pylint: disable=broad-except
            print(f'Failed to get uuid for {sample_group_name}', file=stderr)


@uuids.command(name='orgs')
@add_authorization()
@click.argument('org_names', nargs=-1)
def org_uuids(uploader, org_names):
    """Get UUIDs for the given sample groups."""
    for org_name in org_names:
        try:
            response = uploader.knex.get(f'/api/v1/organizations/getid/{org_name}')
            report_uuid(response['data']['organization_name'],
                        response['data']['organization_uuid'])
        except Exception:  # pylint: disable=broad-except
            print(f'Failed to get uuid for {org_name}', file=stderr)
