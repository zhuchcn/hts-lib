from Bio import SeqIO
import os
import gzip
import argparse
    

def extract_fasta(input_path, output_path, names):
    if os.path.splitext(input_path)[1] == 'gz':
        ih = gzip.open(input_path, 'rt')
    else:
        ih = open(input_path, 'rt')
    
    with open(output_path, 'a') as oh:
        for record in SeqIO.parse(ih, 'fasta'):
            if record.description in names:
                SeqIO.write(record, oh, 'fasta')
    ih.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-file', type=str, default=None,
        help='Input file'
    )
    parser.add_argument(
        '-o', '--output-file', type=str, default=None,
        help='Output file'
    )
    parser.add_argument(
        '-n', '--sequence-name', action='append',
        help='The sequence full name to be extracted'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    extract_fasta(args.input_file, args.output_file, args.sequence_name)