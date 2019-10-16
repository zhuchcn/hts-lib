import re
import gzip
from datetime import datetime
import argparse
import os
from db_mem import NCBITaxonomyInMem


_taxa_levels = [
    'root',
    'kingdom',
    'phylum',
    'class',
    'order',
    'family',
    'genus',
    'species'
]


class TaxaCount():
    reads = {}
    counts = {}
    taxa_levels = _taxa_levels
    
    def __init__(self, input_file, output_prefix, is_gz, path_nodes, path_names):
        self.input_file = input_file
        self.output_prefix = output_prefix
        self.is_gz = is_gz
        self.db = NCBITaxonomyInMem(path_nodes, path_names)
        self.read_txt()
        self.count_reads()
        self.write()

    def read_txt(self):
        if self.is_gz:
            fh = gzip.open(self.input_file, 'rt')
        else:
            fh = open(self.input_file, 'rt')
        print(
            '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
            " ] start reading input"
        )
        for line in fh:
            read_id, tax_name = line.rstrip().split('\t')
            tax_name = tax_name.replace('_', ' ').lower()
            if not self.db.has_tax(tax_name):
                tax_name = ' '.join(tax_name.split(' ')[:2])
            if not self.db.has_tax(tax_name):
                tax_name = tax_name.split(' ')[0]
            if not self.db.has_tax(tax_name):
                continue
            tax_id = self.db.get_tax_id(tax_name)[0]
            rank, level = self.db.get_tax_rank(tax_id)
            
            if read_id not in self.reads:
                self.reads[read_id] = (tax_id, tax_name, rank, level)
            else:
                self.reads[read_id] = self.db.get_common_ancestor(
                    self.reads[read_id][0],
                    tax_id
                )
            while self.reads[read_id][3] not in self.taxa_levels:
                self.reads[read_id] = self.db.get_parent_taxa(
                    self.reads[read_id][0]
                )
        fh.close()
        print(
            '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
            " ] finished reading"
        )
    
    def count_reads(self):
        print(
            '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
            " ] start counting"
        )
        self.counts = {taxa: {} for taxa in self.taxa_levels 
                        if taxa not in ["root", "kingdom"]}
        for read in self.reads.keys():
            tax_id, tax_name, rank, level = self.reads[read]
            while level in self.counts.keys():
                if tax_name not in self.counts[level]:
                    self.counts[level][tax_name] = 1
                else:
                    self.counts[level][tax_name] += 1
                res = self.db.get_parent_taxa(tax_id)
                tax_id, tax_name, rank, level = res
                if level == 'phylum':
                    break
                while level not in self.taxa_levels:
                    res = self.db.get_parent_taxa(tax_id)
                    tax_id, tax_name, rank, level = res
    
    def write(self):
        print(
            '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
            " ] start writing"
        )
        for level, counts in self.counts.items():
            with open(self.output_prefix + level + '.txt', 'w') as fh:
                for taxa, num in counts.items():
                    fh.write(taxa + '\t' + str(num) + '\n')
                

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input-file', type=str, default=None,
        help='Input file'
    )
    parser.add_argument(
        '-o', '--output-prefix', type=str, default=None,
        help='The prefix for output files'
    )
    parser.add_argument(
        '-z', '--zipped', action='store_true',
        help='Whether the file is gzipped'
    )
    parser.add_argument(
        '-d', '--nodes-dump', type=str, default=None,
        help='The NCBI taxonomy dump file for nodes'
    )
    parser.add_argument(
        '-m', '--names-dump', type=str, default=None,
        help='The NCBI taxonomy dump file for names'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    tc = TaxaCount(
        args.input_file,
        args.output_prefix,
        args.zipped,
        args.nodes_dump,
        args.names_dump
    )
    