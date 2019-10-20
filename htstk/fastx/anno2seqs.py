import gzip
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import os
from htstk.utils import log, CommandConfig


def anno2fasta(anno, genome, output, col_chr, col_start, col_end, col_name, 
               skip=0, one_based=False):
    try:
        col_name = [int(i) for i in col_name]
    except ValueError:
        raise ValueError('chol_name must all be int')
    # Parse  the genome. This is going to use a lot of RAM
    log('start reading genome')
    if os.path.splitext(genome)[1] == '.gz':
        with gzip.open(genome, 'rt') as fh:
            genome = SeqIO.to_dict(SeqIO.parse(fh, 'fasta'))
    else:
        genome = SeqIO.to_dict(SeqIO.parse(genome, 'fasta'))

    if os.path.splitext(anno)[1] == '.gz':
        ih = gzip.open(anno, 'rt')
    else:
        ih = open(anno, 'rt')

    log("start extracting sequences")
    oh = open(output, 'a')
    i = 0
    for l in ih:
        if i < skip:
            i += 1
            continue
        l = l.rstrip().rsplit()
        chrom = l[col_chr - 1]
        start = int(l[col_start - 1])
        end = int(l[col_end - 1])
        name = ':'.join([l[i - 1] for i in col_name])
        if not one_based:
            start = start - 1
        if chrom not in genome:
            continue
        record = SeqRecord(
            genome[chrom].seq[start:end],
            id=name,
            name='',
            description=''
        )
        SeqIO.write(record, oh, 'fasta')

    oh.close()
    ih.close()


class Config(CommandConfig):
    name = 'anno2fasta'
    func = anno2fasta
    help = 'Convert a annotation file into a fasta'
    args = [
        (['-a', '--anno-file'], {
            'type': str,
            'default': None,
            'help': 'File path to the annotation file'}),
        (['-g', '--genome-file'], {
            'type': str,
            'default': None,
            'help': 'File path to the genome file'}),
        (['-o', '--output-file'], {
            'type': str,
            'default': None,
            'help': 'File path to the output fasta'}),
        (['-c', '--column-chr'], {
            'type': int,
            'default': None,
            'help': 'Column index for chromosome in the annotation file.'}),
        (['-s', '--column-start'], {
            'type': int,
            'default': None,
            'help': 'Column index for the start position in the annotation '
                    + 'file.'}),
        (['-e', '--column-end'], {
            'type': int,
            'default': None,
            'help': 'Column index for the end position in the annotation '
                    + 'file.'}),
        (['-n', '--column-name'], {
            'action': 'append',
            'help': 'Column index for the name of the gene in the annotation '
                    + 'file.'}),
        (['-k', '--skip-lines'], {
            'type': int,
            'default': 0,
            'help': "Number of lines to skip."}),
        (['-b', '--one-based'], {
            'action': 'store_true',
            'help': 'Whether the annotation file postion starts are one based.'
        })
    ]
    mapper = {
        'anno': 'anno_file',
        'genome': 'genome_file',
        'output': 'output_file',
        'col_chr': 'column_chr',
        'col_start': 'column_start',
        'col_end': 'column_end',
        'col_name': 'column_name',
        'skip': 'skip_lines',
        'one_based': 'one_based'
    }