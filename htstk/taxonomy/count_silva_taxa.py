import os
import re
import gzip


def count_silva_taxa(input_file, output_prefix):
    if os.path.splitext(input_file)[1] == '.gz':
        ih = gzip.open(input_file, 'rt')
    else:
        ih = open(input_file, 'rt')

    