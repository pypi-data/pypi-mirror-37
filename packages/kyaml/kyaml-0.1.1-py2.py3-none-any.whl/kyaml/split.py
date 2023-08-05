import os
import os.path
import yaml

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

def load_combined_manifest(input_file):
    with open(input_file) as infile:
        loaded = yaml.load_all(infile)
        documents = [doc for doc in loaded]
        return documents


def is_directory_empty(path):
    path = str(Path(path).resolve())
    if not os.path.isdir(path):
        raise Exception('{} is not a directory.'.format(path))
    return len(os.listdir(path)) == 0


def write_yaml_document(document, filename, path='.'):
    outfile_name = str(Path(path, filename).resolve())
    with open(outfile_name, 'w') as outfile:
        yaml.dump(document, outfile, default_flow_style=False)


def split_mainfest(combined_file, output_directory):
    """Given an open file handle or stream containing multiple YAML documents
    split them into individual manifest files and store them in the output_directory."""
    if not is_directory_empty(output_directory):
        raise Exception("{} is not empty.".format(output_directory))

    loaded = yaml.load_all(combined_file)
    documents = [doc for doc in loaded]
    for doc in documents:
        unnamed_count = 0
        name = doc.get('metadata', {}).get('name','').lower()
        if name == '':
            name = 'UNNAMED-{:03}'.format(unnamed_count)
            unnamed_count += 1
        kind = doc.get('kind', 'UNKNOWN').lower()
        filename = "{}_{}.yaml".format(name, kind)
        write_yaml_document(doc, filename, path=output_directory)
