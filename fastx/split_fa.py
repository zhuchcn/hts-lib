from Bio import SeqIO
import os
import gzip
from utils import log
import math
import argparse


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
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-file', type=str, default=None,
        help='Input file path. Must be a fasta file.'
    )
    parser.add_argument(
        '-o', '--output-prefix', type=str, default=None,
        help='Output files prefix.'
    )
    parser.add_argument(
        '-r', '--n-record', type=int, default=None,
        help='Number of record in each split file.'
    )
    parser.add_argument(
        '-b', '--n-batch', type=int, default=None,
        help='Number of files to split into. Ignored if --n-record is given.'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    split_fa(
        args.input_file,
        args.output_prefix,
        args.n_record,
        args.n_batch
    )


if __name__ == '__main__':
    main()