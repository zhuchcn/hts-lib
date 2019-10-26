from Bio import SeqIO
import os
import gzip
import re
from htstk.utils import CommandConfig, log
from datetime import datetime, timedelta
    

def extract_fastx(input_path, output_path, names, format, inverse, use_id,
                  verbose, namelist_file=None):
    if format == 'guess':
        if any(input_path.endswith(x) 
                for x in ['fasta', 'fa', 'fasta.gz', 'fa.gz']):
            format = 'fasta'
        elif any(input_path.endswith(x) 
                for x in ['fastq', 'fq', 'fastq.gz', 'fq.gz']):
            format = 'fastq'
        else:
            raise ValueError(
            'Failed to guess the input file format. Please specify.'
        )

    if os.path.splitext(input_path)[1] == '.gz':
        ih = gzip.open(input_path, 'rt')
    else:
        ih = open(input_path, 'rt')
    
    if namelist_file:
        if names:
            log('The -n/--sequence-name was ignored')
        names = []
        with open(namelist_file, 'rt') as fh:
            for l in fh:
                name = l.rstrip()
                names.append(name)
        if verbose:
            log('Reading namelist file finished.')
    names = set(names)

    if verbose:
        log('Start writing sequences.')

    with open(output_path, 'w') as oh:
        records = SeqIO.parse(ih, format)
        for record in records:
            record_name = record.id if use_id else record.description
            save = record_name in names
            if inverse:
                save = not save
            if save:
                if verbose:
                    log(f'Saving {record_name}')
                SeqIO.write(record, oh, format)
    ih.close()


class Config(CommandConfig):
    name = 'extract-fastx'
    func = extract_fastx
    help = 'Extract record(s) from a fasta or fastq file.'
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
            'help': 'The sequence full name to be extracted'}),
        (['-l', '--namelist-file'], {
            'type': str,
            'default': None,
            'help': 'The file contains a list of the names to extract'}),
        (['-f', '--format'], {
            'choices': ['guess', 'fasta', 'fastq'],
            'default': 'guess',
            'help': 'The format of input fastx file.'}),
        (['-v', '--inverse'], {
            'action': 'store_true',
            'help': 'Extract non-matching records'}),
        (['-u', '--use-id'], {
            'action': 'store_true',
            'help': 'Use record ID instead of the whole name to match. This '
                    + 'is useful while processing fastq files'}),
        (['-b', '--verbose'], {
            'action': 'store_true',
            'help': 'Whether to log out more messages.'
        })
    ]
    mapper = {
        'input_path': 'input_file',
        'output_path': 'output_file',
        'names': 'sequence_name',
        'namelist_file': 'namelist_file',
        'format': 'format',
        'inverse': 'inverse',
        'use_id': 'use_id',
        'verbose': 'verbose'
    }
