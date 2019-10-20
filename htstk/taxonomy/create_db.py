import sqlite3
import re
import argparse
from .ncbi_ranks import _TAXONOMIC_RANKS


def create_db(dbfile, nodes_path, names_path):
    create_db_ranks(dbfile)
    create_db_nodes(dbfile, nodes_path)
    create_db_names(dbfile, names_path)


def create_db_ranks(dbfile):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE ranks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            name CHAR(16)
        )
    """)
    for key, val in _TAXONOMIC_RANKS.items():
        c.execute("INSERT INTO ranks (rank, name) VALUES (?, ?)", [val, key])
    
    conn.commit()
    conn.close()


def create_db_names(dbfile, path):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tax_id INTEGER NOT NULL,
            name_txt CHAR(256),
            unique_name CHAR(256),
            name CHAR(32),
            FOREIGN KEY (tax_id) REFERENCES nodes (tax_id)
        )
    """)
    c.execute("""
        CREATE INDEX tax_id_index ON names (tax_id);
    """)
    c.execute("""
        CREATE INDEX name_txt_index ON names (name_txt);
    """)

    with open(path, 'r') as fh:
        for l in fh:
            l = l.rstrip()
            l = re.sub("\t\|$", "", l)
            l = l.split('\t|\t') 
            l[1] = re.sub('[^A-Za-z0-9]', ' ', l[1].lower())
            l[1] = re.sub(' +', ' ', l[1])
            l[1] = l[1].rstrip()
            c.execute("""
                INSERT INTO names (tax_id, name_txt, unique_name, name)
                VALUES (?, ?, ?, ?)
            """, l)
    
    conn.commit()
    conn.close()

def create_db_nodes(dbfile, path):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE nodes (
            tax_id INTEGER PRIMARY KEY,
            parent_tax_id INTEGER,
            rank_id INTEGER,
            embl_code CHAR(2),
            division_id INTEGER,
            inherited_div_flag INTEGER,
            genetic_code_id INTEGER,
            inherited_GC_flag INTEGER,
            mitochondrial_genetic_code_id INTEGER,
            inherited_MGC_flag INTEGER,
            GenBank_hidden_flag INTEGER,
            hidden_subtree_root_flag INTEGER,
            comments VARCHAR,
            FOREIGN KEY (parent_tax_id) REFERENCES name (tax_id),
            FOREIGN KEY (rank_id) REFERENCES rank (id)
        )
    """)
    conn.commit()

    with open(path, "r") as fh:
        for l in fh:
            l = l.rstrip()
            l = re.sub("\t\|$", "", l)
            l = l.split('\t|\t')
            if l[0] == "1" and l[2] == 'no rank':
                l[2] = 'root'
            c.execute("SELECT id FROM ranks WHERE name=(?)", [l[2]])
            l[2] = c.fetchone()[0]
            c.execute("""
                INSERT INTO nodes (
                    tax_id, parent_tax_id, rank_id, embl_code, division_id,
                    inherited_div_flag, genetic_code_id, inherited_GC_flag,
                    mitochondrial_genetic_code_id, inherited_MGC_flag,
                    GenBank_hidden_flag, hidden_subtree_root_flag,
                    comments
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, l)
    conn.commit()
    conn.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--names-dmp", type=str, default=None,
        help="Path to the names.dmp"
    )
    parser.add_argument(
        "-d", "--nodes-dmp", type=str, default=None,
        help="Path to the nodes.dmp"
    )
    parser.add_argument(
        '-o', '--output-path', type=str, default=None,
        help="Path to the output db file"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    create_db(args.output_path, args.nodes_dmp, args.names_dmp)
    