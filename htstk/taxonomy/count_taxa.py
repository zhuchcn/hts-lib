import re
import gzip
import os
import sys
from .db_mem import NCBITaxonomyInMem
from htstk.utils import log, CommandConfig


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
    def __init__(self):
        self.reads = {}
        self.counts = {}
        self.taxa_levels = _taxa_levels

    def load_taxa_dump(self, path_nodes, path_names, no_prune):
        self.db = NCBITaxonomyInMem(path_nodes, path_names)
        if not no_prune:
            self.db.prune_branches(self.taxa_levels)

    def read_txt(self, input_file):
        self.input_file = input_file
        if os.path.splitext(input_file)[1] == '.gz':
            fh = gzip.open(self.input_file, 'rt')
        else:
            fh = open(self.input_file, 'rt')
        log('start reading input')
        for ind, line in enumerate(fh):
            try:
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
            except KeyError as e:
                print(
                    f"A trouble raised when reading line {ind + 1}: {line}",
                    file=sys.stderr
                )
                raise KeyError(e.args[0])

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
        log('finished reading')
    
    def count_reads(self):
        log('start counting')
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
    
    def write(self, output_prefix):
        log('start writing')
        for level, counts in self.counts.items():
            with open(output_prefix + level + '.txt', 'w') as fh:
                for taxa, num in counts.items():
                    fh.write(taxa + '\t' + str(num) + '\n')
        log(f'wrote counts to {len(self.counts)} files')

def count_taxa(path_nodes, path_names, input_file, output_prefix,
               no_prune):
    tc = TaxaCount()
    tc.load_taxa_dump(path_nodes, path_names, no_prune)
    tc.read_txt(input_file)
    tc.count_reads()
    tc.write(output_prefix)


class Config(CommandConfig):
    name = 'count-taxa'
    func = count_taxa
    description = '''
    This script takes a tab separated file with the sequencing read ID and the 
    corresponding NCBI taxonomy label. If a unique ID has more than one 
    taxonomy label, it is assigned to the node higher up in the phylogenetic
    tree. The input file must be a tab delimited file, with the first column
    being the read ID and second being the taxonomy label.
    '''
    args = [
        (['-i', '--input-file'], {
            'type': str,
            'default': None,
            'help': 'Input tab delimited file. The first column must be the '
                    + 'read ID and the second must be the NCBI taxonomy label.'
                    }),
        (['-o', '--output-prefix'], {
            'type': str,
            'default': None,
            'help': 'The prefix for output files.'}),
        (['-d', '--nodes-dump'], {
            'type': str,
            'default': None,
            'help': 'The NCBI taxonomy dump file for nodes'}),
        (['-m', '--names-dump'], {
            'type': str,
            'default': None,
            'help': 'The NCBI taxonomy dump file for names'}),
        (['-p', '--no-prune'], {
            "action": 'store_false',
            'help': 'Wheather prune the branches of the db prior to mapping. '
                    + 'This speed up the mapping process.'
        })
    ]
    mapper = {
        "path_nodes": 'nodes_dump',
        'path_names': 'names_dump',
        'input_file': 'input_file',
        'output_prefix': 'output_prefix',
        'no_prune': 'no_prune'
    }