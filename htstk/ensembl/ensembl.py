from ftplib import FTP
import re
import os
import argparse
import math
import progressbar
from magic import from_file
from htstk.utils import log


class EnsemblFTP():

    def __init__(self):
        self.connect()

    def connect(self):
        self.baseurl = "ftp.ensemblgenomes.org"
        ftp = FTP(self.baseurl)
        ftp.login("anonymous", "")
        self.ftp = ftp
    
    def ls(self, path):
        return self.ftp.nlst(path)
    
    def has_valid_domain(self, domain):
        if domain in ['bacteria', 'fungi', 'metazoa', 'plants', 'protists']:
            return True
        return False
    
    def has_valid_version(self, version):
        if version == 'current':
            return True
        if version in self.ls('pub/release-*'):
            return True
        return False

    def download(self, path, filename, verbose):
        fh = open(filename, "wb")
        log(f"Using url: {self.baseurl + path}")
        
        if verbose:
            size = self.ftp.size(path)
            widgets = [
                'Downloading: ',
                progressbar.Percentage(), ' ',
                progressbar.Bar(marker='#',left='[',right=']'), ' ',
                progressbar.ETA(), ' ',
                progressbar.FileTransferSpeed()
            ]
            pbar = progressbar.ProgressBar(widgets=widgets, maxval=size)
            pbar.start()

            def fh_write(data):
                fh.write(data)
                nonlocal pbar
                pbar += len(data)
            
            self.ftp.retrbinary("RETR " + path, fh_write)
            return
        self.ftp.retrbinary("RETR " + path, fh.write)
    
    def getGenome(self, url, species, outdir, verbose):
        # Skip it if already downloaded. Maybe probromatic.
        # downloaded = [x for x in os.listdir(outdir) \
        #                 if x.split(".")[0] == species]
        # if not force:
        #     if downloaded and \
        #             from_file(os.path.join(outdir, downloaded[0])) != "empty":
        #         print(f"{species} was skipped")
        #         return

        # check if path is valid, create diractory if not
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        # find the fasta.gz file
        files= self.ls(f"{url}/dna")
        file_names = [os.path.basename(x) for x in files]
        r = re.compile(f"{species}\.\S+.dna.toplevel.fa.gz", re.IGNORECASE)
        r_matches = [bool(r.match(x)) for x in file_names]
        path = files[r_matches.index(True)]
        
        filename = os.path.join(outdir, os.path.basename(path))
        self.download(path, filename, verbose) 
    
    def getAnnotation(self, url, species, outdir, _type, verbose):
        # create directory if not exists
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        # stop if annotation type not support
        if _type not in ('gtf', 'gff3'):
            raise ValueError('Only gtf and gff3 are available.')
        if len(self.ls(url)) == 0:
            log('Annotation file not found')
            return
        url = [x for x in self.ls(url) if re.search(f"{_type}.gz", x)]
        if len(url) == 0:
            log(f'Annotation file not found')
            return
        url = url[0]
        filename = os.path.join(outdir, os.path.basename(url))
        self.download(url, filename, verbose)
    
    def getDomainGenomes(self, version, outdir, domain, formats, num_array=1,
                         array_id=1):
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        folders = self.ls(f"pub/{domain}/{version}/fasta")
        k = math.ceil(len(folders) / num_array)
        
        if bool(re.search('_collection$', folders[0])):
            for collection in folders[(array_id-1)*k : array_id*k]:
                for species_url in self.ls(collection):
                    species_name = os.path.basename(species_url)
                    # create the species folder if not exits
                    output_path = os.path.join(
                        outdir, os.path.basename(collection)
                    )
                    if not os.path.exists(output_path):
                        os.mkdir(output_path)
                    # loop through formats
                    for fmt in formats:
                        output_path = os.path.join(output_path, fmt)
                        if fmt == 'fasta':
                            self.getGenome(
                                species_url, species_name, output_path, 
                                verbose=False
                            )
                        else:
                            species_url = species_url.replace(
                                '/fasta/', f"/{fmt}/"
                            )
                            self.getAnnotation(
                                species_url, species_name,
                                output_path, fmt, verbose=False
                            )
        else:
            for species_url in folders:
                species_name = os.path.basename(species_url)
                for fmt in formats:
                    output_path = os.path.join(outdir, species_name)
                    if not os.path.exists(output_path):
                        os.mkdir(output_path)
                    output_paht = os.path.join(output_path, fmt)
                    # loop through formats
                    for fmt in formats:
                        output_path = os.path.join(output_path, fmt)
                        if fmt == 'fasta':
                            self.getGenome(
                                species_url, species_name, output_path, 
                                verbose=False
                            )
                        else:
                            species_url = species_url.replace(
                                '/fasta/', f"/{fmt}/"
                            )
                            self.getAnnotation(
                                species_url, species_name,
                                output_path, fmt, verbose=False
                            )
