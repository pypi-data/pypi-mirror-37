"""MetaGenScope CLI."""

import click

from .. import __version__
from .add_cli import create, add, delete
from .auth_cli import register, login, status
from .get_cli import get
from .run_cli import run
from .upload_cli import upload
from .manage_cli import manage


@click.group()
@click.version_option(__version__)
def main():
    """Use to interact with the MetaGenScope web platform."""
    pass


main.add_command(register)
main.add_command(login)
main.add_command(status)
main.add_command(get)
main.add_command(run)
main.add_command(upload)
main.add_command(create)
main.add_command(add)
main.add_command(delete)
main.add_command(manage)
