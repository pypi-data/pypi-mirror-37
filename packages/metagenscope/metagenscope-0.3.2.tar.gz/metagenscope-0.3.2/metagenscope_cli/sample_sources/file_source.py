"""Samples from a list of files."""

from sys import stderr
from metagenscope_cli.sample_sources import SampleSource

from .constants import UNSUPPORTED_RESULT_TYPES


def parse_file_path(file_path):
    """Extract file metadata from its path."""
    file_name = file_path.split('/')[-1]
    name_components = file_name.split('.')

    sample_name = name_components[0]
    result_type = name_components[1]
    file_type = name_components[2]

    return sample_name, result_type, file_type


class FileSource(SampleSource):
    """Samples from a list of files."""

    def __init__(self, files):
        """Initialize FileSource from list of files."""
        self.files = files

    def get_cataloged_files(self):
        """Return dictionary of files cataloged by sample and type."""
        catalog = {}
        for filename in self.files:
            try:
                sample_name, result_type, file_type = parse_file_path(filename)
            except Exception:  # pylint: disable=broad-except
                print(f'Failed to parse {filename}', file=stderr)
                continue
            if result_type in UNSUPPORTED_RESULT_TYPES:
                continue

            try:
                try:
                    catalog[sample_name][result_type][file_type] = filename
                except KeyError:
                    catalog[sample_name][result_type] = {file_type: filename}
            except KeyError:
                catalog[sample_name] = {result_type: {file_type: filename}}
        return catalog
