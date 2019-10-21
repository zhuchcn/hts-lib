import re
from .ncbi_ranks import _TAXONOMIC_RANKS
from htstk.utils import log


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

class NCBITaxonomyInMem():
    def __init__(self, path_nodes, path_names):
        self.ranks = _TAXONOMIC_RANKS
        self.path_nodes = path_nodes
        self.path_names = path_names
        self.from_dump()

    def from_dump(self):
        log('loading NCBI taxonomy dump')
        # dump names
        names = {}
        with open(self.path_names, 'r') as fh:
            for l in fh:
                l = l.rstrip()
                l = re.sub("\t\|$", "", l)
                l = l.split('\t|\t') 
                if l[-1] != 'scientific name':
                    continue
                l[1] = re.sub('[^A-Za-z0-9]', ' ', l[1].lower())
                l[1] = re.sub(' +', ' ', l[1])
                l[1] = l[1].rstrip()
                names[l[0]] = l[1]
        # dump nodes
        nodes = {}
        with open(self.path_nodes, 'r') as fh:
            for l in fh:
                l = l.rstrip()
                l = re.sub("\t\|$", "", l)
                l = l.split('\t|\t')
                if l[0] == "1" and l[2] == 'no rank':
                    l[2] = 'root'
                nodes[l[0]] = (names[l[0]], l[1], l[2])
        self.names = {}
        for _id, name in names.items():
            self.names.setdefault(name, []).append(_id)
        self.nodes = nodes
    
    def prune_branches(self, taxa_levels=_taxa_levels):
        '''
        Prune the branches of the taxonomy tree, so it takes fewer steps to
        walk to the desired tax level
        '''
        if 'root' not in taxa_levels:
            tax_levels = ['root'] + taxa_levels 

        nodes = {}
        log('start pruning the taxonomic tree')
        for tax_name, node in self.nodes.items():
            tax_id, parent_id, level = node
            if level == 'no rank':
                continue
            if self.ranks[level] < self.ranks['genus'] \
                and level not in taxa_levels:
                    continue
            parent_node = self.get_parent_taxa(parent_id)
            while (parent_node[2] < self.ranks['genus'] 
                and parent_node[3] not in taxa_levels) \
                or parent_node[3] == 'no rank':
                parent_node = self.get_parent_taxa(parent_node[0])
            node = (node[0], parent_node[0], node[2])
            nodes[tax_name] = node

        names = {}
        for tax_id, node in nodes.items():
            tax_name = node[0]
            names.setdefault(tax_name, []).append(tax_id)
        
        self.names = names
        self.nodes = nodes
            

    def get_tax_id(self, tax_name):
        return self.names[tax_name]
    
    def has_tax(self, tax_name):
        return tax_name in self.names
    
    def get_tax_rank(self, tax_id):
        level = self.nodes[tax_id][2]
        return self.ranks[level], level

    def get_parent_taxa(self, tax_id):
        parent_id = self.nodes[tax_id][1]
        parent_node = self.nodes[parent_id]
        parent_rank = self.ranks[parent_node[2]]
        return parent_id, parent_node[0], parent_rank, parent_node[2]
    
    def get_common_ancestor(self, tax_id1, tax_id2):
        node1 = self.nodes[tax_id1]
        tax_name1 = node1[0]
        level1 = node1[2]
        rank1 = self.ranks[level1]

        node2 = self.nodes[tax_id2]
        tax_name2 = node2[0]
        level2 = node2[2]
        rank2 = self.ranks[level2]

        while tax_id1 != tax_id2:
            if rank1 != rank2:
                while rank1 != rank2:
                    if rank1 > rank2:
                        res = self.get_parent_taxa(tax_id1)
                        tax_id1, tax_name1, rank1, level1 = res
                    else:
                        res = self.get_parent_taxa(tax_id2)
                        tax_id2, tax_name2, rank2, level2 = res
            else:
                res = self.get_parent_taxa(tax_id1)
                tax_id1, tax_name1, rank1, level1 = res
                res = self.get_parent_taxa(tax_id2)
                tax_id2, tax_name2, rank2, level2 = res
        
        return tax_id1, tax_name1, rank1, level1
    

if __name__ == '__main__':
    db = NCBITaxonomyInMem('../taxdump/nodes.dmp', '../taxdump/names.dmp')