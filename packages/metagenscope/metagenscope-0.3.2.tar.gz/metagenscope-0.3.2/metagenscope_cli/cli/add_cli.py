"""CLI to create and edit users and organizations."""

from sys import stderr

import click
from requests.exceptions import HTTPError

from .utils import add_authorization


@click.group()
def create():
    """Group create commands together."""
    pass


@create.command(name='user')
@click.argument('username')
@click.argument('user_email')
@click.argument('password')
def create_user(uploader, username, user_email, password):
    """Create a new user."""
    payload = {
        'username': username,
        'email': user_email,
        'password': password,
    }
    try:
        response = uploader.knex.post('/api/v1/auth/register', payload)
        click.echo(response)
    except HTTPError as exc:
        print(f'{exc}', file=stderr)


@create.command(name='org')
@add_authorization()
@click.option('--private/--public', default=True)
@click.argument('group_name')
@click.argument('admin_email')
def create_org(uploader, private, group_name, admin_email):
    """Create a new organization."""
    payload = {
        'name': group_name,
        'admin_email': admin_email,
    }
    if private:
        payload['access_scheme'] = 'private'
    try:
        response = uploader.knex.post('/api/v1/organizations', payload)
        click.echo(response)
    except HTTPError as exc:
        print(f'{exc}', file=stderr)


@click.group()
def add():
    """Group add commands together."""
    pass


@add.command(name='group-to-org')
@add_authorization()
@click.argument('group_name')
@click.argument('org_name')
def add_group_to_org(uploader, group_name, org_name):
    """Add a group to an organization."""
    response = uploader.knex.get(f'/api/v1/organizations/getid/{org_name}')
    org_uuid = response['data']['organization_uuid']
    response = uploader.knex.get(f'/api/v1/sample_groups/getid/{group_name}')
    group_uuid = response['data']['sample_group_uuid']
    payload = {'sample_group_uuid': group_uuid}
    try:
        response = uploader.knex.post(
            f'/api/v1/organizations/{org_uuid}/sample_groups',
            payload
        )
        click.echo(response)
    except HTTPError as exc:
        print(f'{exc}', file=stderr)


@add.command(name='user-to-org')
@add_authorization()
@click.argument('user_id')
@click.argument('org_name')
def add_user_to_org(uploader, user_id, org_name):
    """Add a group to an organization."""
    response = uploader.knex.get(f'/api/v1/organizations/getid/{org_name}')
    org_uuid = response['data']['organization_uuid']
    payload = {'user_id': user_id}
    try:
        response = uploader.knex.post(
            f'/api/v1/organizations/{org_uuid}/users',
            payload
        )
        click.echo(response)
    except HTTPError as exc:
        print(f'{exc}', file=stderr)


@click.group()
def delete():
    """Group delete commands together."""
    pass


@delete.command(name='group')
@add_authorization()
@click.argument('group_name')
def delete_group(uploader, group_name):
    """Add a group to an organization."""
    response = uploader.knex.get(f'/api/v1/sample_groups/getid/{group_name}')
    group_uuid = response['data']['sample_group_uuid']
    click.echo(f'{group_name} :: {group_uuid}')
    response = uploader.knex.delete(f'/api/v1/sample_groups/{group_uuid}')
    click.echo(response)
