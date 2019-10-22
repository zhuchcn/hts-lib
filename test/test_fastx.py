import unittest
import os
import shutil
import subprocess
from Bio import SeqIO


class TestFastx(unittest.TestCase):

    def setUp(self):
        self.output_dir = '_test_output'
        os.mkdir('_test_output')
    
    def tearDown(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)
    
    def test_help(self):
        '''
        Test that the main help message is printed
        '''
        res = subprocess.run(
            'python -m htstk.fastx'.split(),
            capture_output=True
        )
        stderr = res.stderr.decode('utf-8')
        self.assertTrue(stderr.startswith('usage: '))
        self.assertTrue('HTS Fastx Processor' in stderr)
    
    def test_extract_fatsta(self):
        '''
        Test that the extract_fa.py is extracting the specified sequence
        '''
        seq_name = "L1MC5a_LINE/L1_chr1_11505_11675"
        input_file = os.path.join('test', 'data', 'test.fa')
        output_file = os.path.join(self.output_dir, 'test_extract_fa.fa')
        cmd = f'''
        python -m htstk.fastx extract-fastx 
            --input-file {input_file}
            --output-file {output_file}
            --sequence-name {seq_name}
        '''
        subprocess.run(cmd.split())
        seqs = list(SeqIO.parse(output_file, 'fasta'))
        self.assertEqual(len(seqs), 1)
        self.assertEqual(seqs[0].id, seq_name)

    def test_extract_fatstq(self):
        '''
        Test that the extract_fa.py is extracting the specified sequence
        '''
        input_file = os.path.join('test', 'data', 'test.fastq')
        output_file = os.path.join(self.output_dir, 'test_extract_fq.fq')
        namelist_file = os.path.join('test', 'data', 'split_fastq_ids.txt')
        cmd = f'''
        python -m htstk.fastx extract-fastx 
            --input-file {input_file}
            --output-file {output_file}
            --namelist-file {namelist_file}
            --use-id
        '''
        subprocess.run(cmd.split())
        seqs = list(SeqIO.parse(output_file, 'fastq'))
        self.assertEqual(len(seqs), 4)

        cmd = f'''
        python -m htstk.fastx extract-fastx 
            --input-file {input_file}
            --output-file {output_file}
            --namelist-file {namelist_file}
            --use-id -v
        '''
        subprocess.run(cmd.split())
        seqs = list(SeqIO.parse(output_file, 'fastq'))
        self.assertEqual(len(seqs), 4)

    def test_split_fa(self):
        input_file = os.path.join('test', 'data', 'test.fa')
        output_prefix = os.path.join(self.output_dir, 'test_split_fa_')
        cmd = f'''
        python -m htstk.fastx split-fasta
            --input-file {input_file}
            --output-prefix {output_prefix}
            --n-record 5
        '''
        subprocess.run(cmd.split())
        for file in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, file)
            seqs = list(SeqIO.parse(file_path, 'fasta'))
            self.assertEqual(len(seqs), 5)
    
    def test_anno2fasta(self):
        anno_file = os.path.join('test', 'data', 'anno_rm_hg38.txt')
        genome_file = os.path.join('test', 'data', 'hg38_chr1_trunc.fa')
        output_file = os.path.join(self.output_dir, 'anno2fasta.fa')
        cmd = f'''
        python -m htstk.fastx anno2fasta
            --anno-file {anno_file}
            --genome-file {genome_file}
            --output-file {output_file}
            --column-chr 5
            --column-start 6
            --column-end 7
            --column-name 10
            --skip-lines 3
        '''
        subprocess.run(cmd.split())
        seqs = list(SeqIO.parse(output_file, 'fasta'))
        self.assertEqual(len(seqs), 10)