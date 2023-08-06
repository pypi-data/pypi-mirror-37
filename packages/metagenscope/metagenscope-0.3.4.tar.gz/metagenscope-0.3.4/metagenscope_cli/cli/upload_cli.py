"""CLI to upload data to a MetaGenScope Server."""

from sys import stderr
import click

from metagenscope_cli.sample_sources.data_super_source import DataSuperSource
from metagenscope_cli.sample_sources.file_source import FileSource

from .utils import batch_upload, add_authorization, parse_metadata


@click.group()
def upload():
    """Handle different types of uploads."""
    pass


@upload.command()
@add_authorization()
@click.argument('metadata_csv')
@click.argument('sample_names', nargs=-1)
def metadata(uploader, metadata_csv, sample_names):
    """Upload a CSV metadata file."""
    parsed_metadata = parse_metadata(metadata_csv, sample_names)
    for sample_name, metadata_dict in parsed_metadata.items():
        payload = {
            'sample_name': str(sample_name),
            'metadata': metadata_dict,
        }
        try:
            response = uploader.knex.post('/api/v1/samples/metadata', payload)
            click.echo(response)
        except Exception:  # pylint:disable=broad-except
            print(f'[upload-metadata-error] {sample_name}', file=stderr)


@upload.command()
@add_authorization()
@click.option('-u', '--group-uuid', default=None)
@click.option('-d', '--datasuper-group', default=None)
@click.option('-g', '--group-name', default=None)
def datasuper(uploader, group_uuid, datasuper_group, group_name):
    """Upload all samples from DataSuper repo."""
    sample_source = DataSuperSource(group=datasuper_group)
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group_uuid, upload_group_name=group_name)


@upload.command()
@add_authorization()
@click.option('-u', '--group-uuid', default=None)
@click.option('-g', '--group-name', default=None)
@click.option('-m/-l', '--manifest/--file-list', default=False)
@click.argument('result_files', nargs=-1)
def files(uploader, group_uuid, group_name, manifest, result_files):
    """Upload all samples from llist of tool result files."""
    if manifest:
        result_file_list = []
        for result_manifest in result_files:
            with open(result_manifest) as rmf:
                for line in rmf:
                    result_file_list.append(line.strip())
        result_files = result_file_list
    sample_source = FileSource(files=result_files)
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group_uuid, upload_group_name=group_name)
