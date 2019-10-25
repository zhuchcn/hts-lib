import unittest
import os
import shutil


class TestCase(unittest.TestCase):
    def setUp(self):
        self.output_dir = '_test_output'
        os.mkdir('_test_output')
    
    def tearDown(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)