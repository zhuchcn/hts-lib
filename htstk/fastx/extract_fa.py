from Bio import SeqIO
import os
import gzip
from htstk.utils import CommandConfig
    

def extract_fasta(input_path, output_path, names):
    if os.path.splitext(input_path)[1] == '.gz':
        ih = gzip.open(input_path, 'rt')
    else:
        ih = open(input_path, 'rt')
    
    with open(output_path, 'a') as oh:
        for record in SeqIO.parse(ih, 'fasta'):
            if record.description in names:
                SeqIO.write(record, oh, 'fasta')
    ih.close()


class Config(CommandConfig):
    name = 'extract-fasta'
    func = extract_fasta
    help = 'Extract a specific record of a fasta files by a given record ID'
    args = [
        (['-i', '--input-file'], {
            'type': str,
            'default': None,
            'help': 'Input file'}),
        (['-o', '--output-file'], {
            'type': str,
            'default': None,
            'help': 'Output file'}),
        (['-n', '--sequence-name'], {
            'action': 'append',
            'help': 'The sequence full name to be extracted'
        })
    ]
    mapper = {
        'input_path': 'input_file',
        'output_path': 'output_file',
        'names': 'sequence_name'
    }