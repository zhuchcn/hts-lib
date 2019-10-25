import os
import unittest
import subprocess
import shutil
from . import TestCase


class TestEnsembl(TestCase):
    def test_versions(self):
        cmd = '''
        python -m htstk.ensembl versions
        '''
        versions = subprocess.run(
            cmd.split(), capture_output=True, encoding='utf-8'
        )
        for v in versions.stdout.split():
            self.assertTrue(v.startswith('release-'))
    
    def test_species(self):
        # test that the domain is required
        cmd = 'python -m htstk.ensembl species -v current'
        res = subprocess.run(
            cmd.split(), capture_output=True, encoding='utf-8'
        )
        msg = 'error: the following arguments are required:'
        self.assertTrue(res.stderr.find(msg) != -1)
        
        # test that a valid domain is required
        cmd = 'python -m htstk.ensembl species fungus'
        res = subprocess.run(
            cmd.split(), capture_output=True, encoding='utf-8'
        )
        msg = 'Ensembl does not have this domain: '
        self.assertTrue(res.stderr.find(msg) != -1)

        # test that it goes through
        cmd = 'python -m htstk.ensembl species fungi'    
        subprocess.run(cmd.split(), capture_output=True)
    
    def test_download(self):
        cmd = 'python -m htstk.ensembl download -d fungus blumeria_graminis'
        res = subprocess.run(
            cmd.split(), capture_output=True, encoding='utf-8'
        )
        msg = 'Ensembl does not have this domain: '
        self.assertTrue(res.stderr.find(msg) != -1)

        cmd = '''
        python -m htstk.ensembl download
            -t gff
            -d fungi
            blumeria_graminis
        '''
        res = subprocess.run(
            cmd.split(), capture_output=True, encoding='utf-8'
        )
        self.assertTrue(res.stderr.find('invalid choice') != -1)
        cmd = f'''
        python -m htstk.ensembl download
            -d fungi
            -t fasta
            -o {self.output_dir}
            blumeria_graminis
        '''
        subprocess.run(cmd.split())
