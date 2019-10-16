import sqlite3


class NCBITaxonomy():
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self._connect()
    
    def _connect(self):
        self.conn = sqlite3.connect(self.dbfile)

    def has_tax(self, tax_name):
        return len(self.get_tax_id(tax_name)) > 0
    
    def get_tax_id(self, tax_name):
        # conn = sqlite3.connect(self.dbfile)
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT tax_id FROM names 
            WHERE name='scientific name' AND name_txt=?
            """,
            [tax_name]
        )
        res = [r[0] for r in cur.fetchall()]
        # conn.close()
        return res
    
    def get_tax_name(self, tax_id, name_type="scientific name"):
        # conn = sqlite3.connect(self.dbfile)
        cur = self.conn.cursor()
        cur.execute(
            "SELECT name_txt FROM names WHERE tax_id=? AND name=?",
            [tax_id, name_type]
        )
        res = [r[0] for r in cur.fetchall()]
        # conn.close()
        return res
    
    def get_rank_level(self, level):
        cur = self.conn.cursor()
        cur.execute("SELECT rank FROM ranks WHERE name = ?", [level])
        return cur.fetchone()[0]
    

    def get_tax_rank(self, tax_id):
        # conn = sqlite3.connect(self.dbfile)
        cur = self.conn.cursor()
        cur.execute(
            """
                SELECT ranks.rank, ranks.name FROM nodes 
                JOIN ranks ON nodes.rank_id = ranks.id
                WHERE nodes.tax_id = ?
            """,
            [tax_id]
        )
        res = cur.fetchone()
        # conn.close()
        return res
    
    def get_parent_taxa(self, tax_id):
        # tax_id = self.get_tax_id(tax_name)[0]
        # conn = sqlite3.connect(self.dbfile)
        cur = self.conn.cursor()
        cur.execute(
            "SELECT parent_tax_id FROM nodes WHERE tax_id = ?",
            [tax_id]
        )
        parent_id = cur.fetchone()[0]
        # conn.close()
        parent_tax = self.get_tax_name(parent_id)[0]
        parent_rank, parent_level = self.get_tax_rank(parent_id)
        return parent_id, parent_tax, parent_rank, parent_level
    
    def get_taxa_at(self, tax_name, level):
        tax_rank, tax_level = self.get_tax_rank(tax_name)
        rank = self.get_rank_level(level)
        # stop if the given taxa is higher
        if tax_rank < rank:
            raise ValueError('input level must be higher than tax_name')
        while tax_rank > rank:
            tax_name, tax_rank, tax_level = self.get_parent_taxa(tax_name)
        # this means the tax_name given does not have a taxonomy label at the 
        # given level
        if tax_rank < rank:
            return None
        return tax_name, tax_rank, tax_level
        

    def get_common_ancestor(self, tax_id1, tax_id2):
        tax_name1 = self.get_tax_name(tax_id1)[0]
        tax_name2 = self.get_tax_name(tax_id2)[0]
        rank1, level1 = self.get_tax_rank(tax_id1)
        rank2, level2 = self.get_tax_rank(tax_id2)
        
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


if __name__ == "__main__":
    from datetime import datetime
    t1 = datetime.utcnow()
    taxa = NCBITaxonomy('taxdump.sqlite3')
    print(taxa.get_common_ancestor('bacillus campisalis', 'bacillus cereus'))
    t2 = datetime.utcnow()
    print(t2 - t1)