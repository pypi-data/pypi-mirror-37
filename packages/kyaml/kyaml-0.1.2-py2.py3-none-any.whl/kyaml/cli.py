
import click

from .split import split_mainfest

@click.group(name='kyaml')
def kyaml():
    """Utility to manipulate Kubernetes YAML files."""

@kyaml.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('--output-dir', '-o', default='./output', type=click.Path(exists=True, file_okay=False, resolve_path=True))
def split(infile, output_dir):
    """Split a single multi-mainfest YAML file into multiple files."""
    split_mainfest(infile, output_dir)