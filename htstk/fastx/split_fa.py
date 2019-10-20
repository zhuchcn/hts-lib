from Bio import SeqIO
import os
import gzip
from htstk.utils import log, CommandConfig
import math


def split_fa(input_file, output_prefix, n_record=None, n_batch=None):
    if os.path.splitext(input_file)[1] == '.gz':
        ih = gzip.open(input_file, 'rt')
    else:
        ih = open(input_file, 'rt')
    
    if n_record:
        if n_batch:
            log("n_batch is ignored")        
    elif n_batch:
        n = 0
        for line in ih:
            if line.startswith(">"):
                n += 1
        n_record = math.ceil( n / n_batch )
    else:
        raise ValueError('At least one of n_record or n_batch must be given.')
    
    split_fa_n_record(ih, output_prefix, n_record)
    ih.close()

def split_fa_n_record(ih, output_prefix, n_record):
    i = 0
    j = 1
    seqs = []
    def write():
        log(f"Writing {len(seqs)} records to {output_prefix}{j}.fasta")
        with open(f"{output_prefix}{j}.fasta", 'w') as oh:
            SeqIO.write(seqs, oh, 'fasta')
    for record in SeqIO.parse(ih, 'fasta'):
        seqs.append(record)
        i += 1
        if i >= n_record:
            write()
            i = 0
            j += 1
            seqs = []
    if i != 0:
        write()


class Config(CommandConfig):
    name = 'split-fasta'
    func = split_fa
    help = 'Split fasta files into batches'
    args = [
        (['-i', '--input-file',], {
            "type": str,
            "default": None,
            "help": 'Input file path. Must be a fasta file.'}),
        (['-o', '--output-prefix'], {
            "type": str,
            "default": None,
            "help": 'Output files prefix.'}),
        (['-r', '--n-record'], {
            "type": int,
            "default": None,
            "help": 'Number of record in each split file.'}),
        (['-b', '--n-batch'], {
            "type": int,
            "default": None,
            "help": 'Number of files to split into. Ignored if --n-record is '
                    + 'given.'})]
    mapper = {
        'input_file': 'input_file',
        'output_prefix': 'output_prefix',
        'n_record': 'n_record',
        'n_batch': 'n_batch'
    }
